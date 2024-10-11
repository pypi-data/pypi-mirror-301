"""
Statistical evaluation (by a course organizer/course developer) of the progress of 
an entire course cohort.

Goals:
- Understand difficulty level distribution across the students.
- Identify tasks with too-low or too-high time value (via worktime) or difficulty (via resubmissions).
- Understand re-submission behavior patterns (per people, per tasks, over time).
- Understand work time patterns (workdays, weekly trends, etc.)
"""
import contextlib
import datetime as dt
import glob
import os

import argparse_subcommand as ap_sub

import base as b
import git
import sdrl.course
import sdrl.participant

meaning = """Statistical evaluation of the progress of an entire course cohort."""


def add_arguments(subparser: ap_sub.ArgumentParser):
    subparser.add_argument('--log', default="INFO", choices=b.loglevels.keys(),
                           help="Log level for logging to stdout (default: INFO)")


class Repo:
    reponame: str


class Commit:
    reponame: str
    timestamp: dt.datetime
    commit_id: str
    by_instructor: bool

class CourseDummy(sdrl.course.Course):
    blockmacro_topmatter = dict()
    
    def __init__(self, *args, **kwargs):
        pass  # we are a truly dumb Dummy!


def execute(pargs: ap_sub.Namespace):
    b.set_loglevel(pargs.log)
    b.info("evaluator, voilà!")
    pull_all_repos()
    collect_commit_metadata()


def pull_all_repos() -> list[str]:
    """Visit subdirs, pull repo (if any), return subdir names with a student.yaml."""
    repolist = []
    # ----- find repolist:
    for path in glob.glob("*"):
        if not os.path.isdir(path):
            continue  # skip files and potential exotic stuff
        if not os.path.isdir(os.path.join(path, '.git')):
            continue  # skip directories not containing a repo
        repolist.append(path)
    repolist.sort()
    # ----- pull each repo:
    b.info(f"pulling {len(repolist)} git repos")
    progressbar = b.get_progressbar(len(repolist))
    for repo in repolist:
        with contextlib.chdir(repo):
            git.pull(silent=True)
            next(progressbar)
    return repolist


def collect_commit_metadata():
    ...


def collect_submisson_yaml_metadata():
    ...

