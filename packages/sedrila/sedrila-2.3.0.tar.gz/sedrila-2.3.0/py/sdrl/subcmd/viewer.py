import dataclasses
import functools
import html
import http.server
import io
import os
import posixpath
import re
import sys
import typing as tg
import urllib.parse

import argparse_subcommand as ap_sub

import base as b
import sdrl.argparser
import sdrl.constants as c
import sdrl.course
import sdrl.macros as macros
import sdrl.macroexpanders as macroexpanders
import sdrl.markdown as md
import sdrl.participant

meaning = """Specialized webserver for locally viewing contents of a student repo work directory."""


def add_arguments(subparser):
    subparser.add_argument('--port', '-p', type=int, default=8080,
                           help="webserver will listen on this port (default: 8080)")
    subparser.add_argument('--instructor', '-i', action='store_true', default=False,
                           help=f"generate task links to the instructor versions (not the student versions)")


class CourseDummy(sdrl.course.Course):
    blockmacro_topmatter = dict()
    
    def __init__(self, *args, **kwargs):
        pass  # we are a truly dumb Dummy!


def execute(pargs: ap_sub.Namespace):
    b.set_loglevel('INFO')
    b.info(f"Webserver starts. Visit 'http://localhost:{pargs.port}/'. Terminate with Ctrl-C.")
    b.set_register_files_callback(lambda s: None)
    macroexpanders.register_macros(CourseDummy())  # noqa
    server = SedrilaServer(('', pargs.port), SedrilaHTTPRequestHandler, pargs=pargs)
    server.serve_forever()


def render_markdown(info: 'Info', infile, outfile):
    markup_body = infile.read().decode()
    markup = f"# {info.lastname}:{info.fullpath}\n\n{info.byline}\n\n{markup_body}\n"
    do_render_markdown(info, markup, outfile)


def render_prot(info: 'Info', infile, outfile):
    markup = (f"# {info.lastname}:{info.fullpath}\n\n{info.byline}\n\n"
              f"[PROT::{info.fullpath}]\n")
    do_render_markdown(info, markup, outfile)


def render_sourcefile(language: str, info: 'Info', infile, outfile):
    src = infile.read().decode()
    markup = (f"# {info.title}\n\n{info.byline}\n\n"
              f"```{language}\n"
              f"{src}\n"
              f"```\n")
    do_render_markdown(info, markup, outfile)


def just_copyfile(copyfilefunc, info, infile, outfile):
    copyfilefunc(infile, outfile)


def do_render_markdown(info: 'Info', markup: str, outfile):
    template = """<!DOCTYPE HTML>
      <html>
      <head>
        <meta charset="{enc}">
        {csslinks}
        <title>{title}</title>
      </head>
      <body>
        {body}
      </body>
      </html>
    """
    macros.switch_part("viewer")
    mddict = md.render_markdown(info.fullpath, info.basename, markup, b.Mode.STUDENT, dict())
    htmltext = template.format(enc='utf8', csslinks=info.csslinks,
                               title=f"{info.lastname}:{info.basename}", body=mddict['html'])
    outfile.write(htmltext.encode())


@dataclasses.dataclass
class Info:
    pargs: ap_sub.Namespace
    basename: str
    fullpath: str
    lastname: str
    byline: str
    csslinks: str

    @property
    def title(self) -> str:
        return f"{self.lastname}:{self.basename}"


class SedrilaServer(http.server.HTTPServer):
    pargs: ap_sub.Namespace
    student_name: str = "N.N."
    lastname: str = "N.N."
    partner_name: str = ""
    course_url: str = ""
    submissionitems: dict
    submission_re: str

    def __init__(self, *args, **kwargs):
        self.server_version = f"SedrilaHTTP/{sdrl.argparser.SedrilaArgParser.get_version()}"
        self.pargs = kwargs.pop('pargs')
        try:
            student = sdrl.participant.Student()
            self.student_name = student.student_name
            mm = re.search(r"(\w+)$", self.student_name)
            self.lastname = mm.group(1) if mm else "??"
            self.partner_name = student.partner_student_name
            self.course_url = student.course_url
        except b.CritialError:
            pass  # fall back to defaults
        if os.path.exists(c.SUBMISSION_FILE):
            self.submissionitems = b.slurp_yaml(c.SUBMISSION_FILE)
            self.submission_re = self._matcher_regexp(self.submissionitems.keys())
        else:
            self.submissionitems = dict()
            self.submission_re = None
        super().__init__(*args, **kwargs)

    def version_string(self) -> str:
        return self.server_version
    
    def _matcher_regexp(self, items: tg.Iterable[str]) -> str:
        return '|'.join([re.escape(item) for item in items])

class SedrilaHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve nice directory listings, serve rendered versions of some file types and files as-is otherwise."""
    server: SedrilaServer
    renderer: tg.Callable[[tg.Any, tg.Any], None]  # for-read() file, for-write() file
    extensions_map = _encodings_map_default = {
        '.gz': 'application/gzip',
        '.Z': 'application/octet-stream',
        '.bz2': 'application/x-bzip2',
        '.xz': 'application/x-xz',
    }
    how_to_render = dict(  # suffix -> (mimetype, renderfunc)
        md=('text/html', render_markdown),
        c=('text/html', functools.partial(render_sourcefile, 'c')),
        css=('text/html', functools.partial(render_sourcefile, 'css')),
        html=('text/html', functools.partial(render_sourcefile, 'html')),
        json=('text/html', functools.partial(render_sourcefile, 'json')),
        java=('text/html', functools.partial(render_sourcefile, 'java')),
        py=('text/html', functools.partial(render_sourcefile, 'python')),
        sh=('text/html', functools.partial(render_sourcefile, 'sh')),
        yaml=('text/html', functools.partial(render_sourcefile, 'yaml')),
        prot=('text/html', render_prot),
    )

    def send_head(self):  # simplified: no caching, no Content-Length
        path = self.translate_path(self.path)
        f = None  # noqa
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                self.send_response(http.HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            return self.list_directory(path)
        ctype = self.guess_type(path)
        if path.endswith("/"):
            self.send_error(http.HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            f = open(self.sedrila_actualpath(path), 'rb')
        except (OSError, FileNotFoundError):
            self.send_error(http.HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def list_directory(self, path):
        try:
            dirlist = os.listdir(path)
        except OSError:
            self.send_error(
                http.HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        dirlist.sort(key=lambda a: a.lower())
        pairslist = [(name, os.path.join(path, name)) for name in dirlist]
        dirpairs = [(name, fullname) for name, fullname in pairslist 
                    if os.path.isdir(fullname)]
        filepairs = [(name, fullname) for name, fullname in pairslist 
                     if os.path.isfile(fullname)]
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        info = Info(pargs=self.server.pargs,
                    basename=displaypath, fullpath=displaypath, 
                    lastname=self.server.lastname, byline=self.sedrila_byline(),
                    csslinks=self.sedrila_csslinks())
        r.append('<!DOCTYPE HTML>')
        r.append('<html>')
        r.append('<head>')
        r.append(f'<meta charset="{enc}">')
        r.append(info.csslinks)
        r.append(f'<title>{info.title}</title>\n</head>')
        r.append(f'<body>\n<h1>{info.title}</h1>')
        r.append(f'<p>{info.byline}</p>')
        if filepairs:
            r.append('<hr>\n<h3>Files</h3>\n<ol>')
            r.extend(self.sedrila_linkitems(filepairs, info))
            r.append('</ol>')
        if dirpairs:
            r.append('<hr>\n<h3>Directories</h3>\n<ol>')
            r.extend(self.sedrila_linkitems(dirpairs, info, dirs=True))
            r.append('</ol>')
        r.append('</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.renderer = functools.partial(just_copyfile, super().copyfile, info)
        return f

    def copyfile(self, source, outputfile):
        """Render file-like object source into file-like destination outputfile."""
        self.renderer(source, outputfile)

    def guess_type(self, path):
        base, ext = posixpath.splitext(path)
        basename = os.path.basename(path)
        info = Info(pargs=self.server.pargs,
                    basename=basename, fullpath=os.path.relpath(path), 
                    lastname=self.server.lastname, byline=self.sedrila_byline(),
                    csslinks=self.sedrila_csslinks())
        if ext and ext[1:] in self.how_to_render:
            mimetype, renderfunc = self.how_to_render[ext[1:]]  # lookup without the dot
            self.renderer = functools.partial(renderfunc, info)
            return mimetype
        elif ext == ".htmlpage":  # special case
            self.renderer = functools.partial(just_copyfile, super().copyfile, info)
            return 'text/html'
        else:
            self.renderer = functools.partial(just_copyfile, super().copyfile, info)
        return super().guess_type(path)

    def sedrila_actualpath(self, path: str) -> str:
        """Convert *.htmlpage to *.html (special case)."""
        actual = re.sub(r"\.htmlpage$", ".html", path)
        # print(f"actualpath: {path} -> {actual}")
        return actual

    def sedrila_byline(self) -> str:
        partner = f" (and {self.server.partner_name})" if self.server.partner_name else ""
        return f"{self.server.student_name}{partner}"

    def sedrila_csslinks(self) -> str:
        if not self.server.course_url:
            return ""
        return (f'<link href="{self.server.course_url}/sedrila.css" rel="stylesheet">\n'
                f'<link href="{self.server.course_url}/local.css" rel="stylesheet">\n'
                f'<link href="{self.server.course_url}/codehilite.css" rel="stylesheet">\n')
    
    def sedrila_linkitems(self, pairs: tg.Iterable[tuple[str, str]], info: Info, dirs=False) -> tg.Iterable[str]:
        res = []
        submission_re = self.server.submission_re
        for name, fullname in pairs:
            submission_mm = submission_re and re.match(submission_re, name)
            tasklink = ""
            if self.is_sedrila_invisible(name) or os.path.islink(fullname):
                continue  # skip dotfiles and symlinks
            if not dirs and name.endswith('.html'):
                htmlpagelink = f"&#9;&#9;&#9;<a href='{name}page' class='vwr-htmlpagelink'>page</a>"
            else:
                htmlpagelink = ""
            if dirs:
                cssclass = 'vwr-dirlink'
            elif submission_mm:
                cssclass = 'vwr-filelink-submission'
                matchtext = submission_mm.group()
                instructordir = (f"{c.AUTHOR_OUTPUT_INSTRUCTORS_DEFAULT_SUBDIR}/" 
                                 if info.pargs.instructor else "")
                taskurl = f"{self.server.course_url}/{instructordir}{matchtext}.html"
                tasklink = f"&#9;&#9;&#9;<a href='{taskurl}' class='vwr-tasklink'>Task '{matchtext}'</a>"
            else:
                cssclass = 'vwr-filelink'
            href = urllib.parse.quote(name, errors='surrogatepass')
            linktext = html.escape(name, quote=False)
            res.append(f"  <li class='vwr-pre'><a href='{href}' class='{cssclass}'>{linktext}</a>"
                       f"{tasklink}{htmlpagelink}</li>")
        return res

    @staticmethod
    def is_sedrila_invisible(name: str) -> bool:
        return name.startswith('.')  # TODO 2: use https://pypi.org/project/gitignore-parser/
