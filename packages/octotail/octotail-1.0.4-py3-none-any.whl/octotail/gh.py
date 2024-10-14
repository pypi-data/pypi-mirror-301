"""GitHub actor."""

import re
from contextlib import suppress
from subprocess import CalledProcessError, check_output
from threading import Event
from typing import NamedTuple, Set

from github import Repository
from github.WorkflowRun import WorkflowRun
from pykka import ActorRef, ThreadingActor

from octotail.utils import Ok, Result, Retry, debug, log, retries

VALID_STATI = ["queued", "in_progress", "requested", "waiting", "action_required"]


class WorkflowDone(NamedTuple):
    """Workflow done message."""

    conclusion: str


class JobDone(NamedTuple):
    """Job done message."""

    job_id: int
    job_name: str
    conclusion: str


class RunWatcher(ThreadingActor):
    """Watches for changes in a GitHub Actions run."""

    wf_run: WorkflowRun
    mgr: ActorRef
    stop: Event

    _new_jobs: Set[int] = set()
    _concluded_jobs: Set[int] = set()

    def __init__(self, mgr: ActorRef, wf_run: WorkflowRun):
        super().__init__()
        self.wf_run = wf_run
        self.mgr = mgr
        self.stop = mgr.proxy().stop_event.get()

    def watch(self) -> None:
        while not self.stop.is_set():
            self.wf_run.update()

            with suppress(Exception):
                for job in self.wf_run.jobs():
                    if job.conclusion and not job.id in self._concluded_jobs:
                        self.mgr.tell(JobDone(job.id, job.name, job.conclusion))
                        self._concluded_jobs.add(job.id)
                        continue
                    if not job.id in self._new_jobs.union(self._concluded_jobs):
                        self.mgr.tell(job)
                        self._new_jobs.add(job.id)

            if self.wf_run.conclusion:
                self.mgr.tell(WorkflowDone(self.wf_run.conclusion))

            self.stop.wait(2)
        debug("exiting")


@retries(10, 0.5)
def get_active_run(
    repo: Repository, head_sha: str, workflow_name: str
) -> Result[WorkflowRun] | Retry:
    with suppress(Exception):
        runs = repo.get_workflow_runs(head_sha=head_sha)
        _runs = [r for r in runs if r.name == workflow_name]
        if not _runs:
            return Retry()

        run = _runs[0]
        if not run.status in VALID_STATI:
            log(f"cannot process run in state: '{run.status}'")
            log(f"try:\n\n\tgh run view {run.id} --log\n")
            log(f"or try browsing to:\n\n\t{run.url}\n")
            return RuntimeError("invalid run state")

        return Ok(run)

    return Retry()


def guess_repo() -> str | None:
    try:
        remotes = check_output(["git", "remote"]).decode().strip().splitlines()
    except CalledProcessError as e:
        log(f"fatal: couldn't list git remotes: {e}")
        return None
    repos = list(filter(None, map(_guess_repo, remotes)))
    if len(repos) > 1:
        log("fatal: found multiple remotes with github URLs")
    return repos[0] if repos else None


def _guess_repo(remote: str) -> str | None:
    with suppress(Exception):
        origin = check_output(f"git remote get-url {remote}".split()).decode().strip()
        if (match := re.search(r"^git@github.com:([^.]+).git$", origin)) is not None:
            return match.group(1)
    return None
