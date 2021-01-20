import logging
import os
import pathlib
import pygit2
import re


log = logging.getLogger(__name__)


def filter_repos(repos, owner=None, repo=None, exclude_owner=None,
                 exclude_repo=None, exclude_forks=False):
    if owner:
        repos = [r for r in repos if re.search(owner, r.owner.login)]
    if repo:
        repos = [r for r in repos if re.search(repo, r.name)]
    if exclude_owner:
        repos = [r for r in repos
                 if not re.search(exclude_owner, r.owner.login)]
    if exclude_repo:
        repos = [r for r in repos if not re.search(exclude_repo, r.name)]
    if exclude_forks:
        repos = [r for r in repos if not r.fork]
    return repos


def clone_path(root, repo):
    return os.path.join(root, repo.owner.login, f"{repo.name}.git")


def mkdir_p(path):
    if os.path.exists(path):
        return False
    pathlib.Path(path).mkdir(parents=True)
    return True


# FIXME: Support other authentication methods (e.g. ssh key, user/pass)
def git_credentials_callback(token=None):
    credentials = pygit2.UserPass(token, "")
    return pygit2.RemoteCallbacks(credentials=credentials)


def git_mirror_remote(repo, name, url):
    remote = repo.remotes.create(name, url, "+refs/*:refs/*")
    repo.config[f"remote.{name}.mirror"] = True
    return remote


# FIXME: Support other URL types (e.g. ssh)
def clone_repo(repo, path, git_callbacks=None, dry_run=False):
    if os.path.isdir(path):
        return False

    url = repo.clone_url
    log.info(f"Cloning: {url} -> {path}")
    if dry_run:
        return False

    mkdir_p(path)
    return pygit2.clone_repository(
        url,
        path,
        callbacks=git_callbacks,
        bare=True,
        remote=git_mirror_remote
    )


def fetch_repo(path, git_callbacks=None, dry_run=False):
    if not os.path.isdir(path):
        return False

    repo = pygit2.Repository(path)
    remote = repo.remotes["origin"]
    log.info(f"Fetching: {remote.url} -> {path}")
    if dry_run:
        return False

    return remote.fetch(callbacks=git_callbacks, prune=pygit2.GIT_FETCH_PRUNE)
