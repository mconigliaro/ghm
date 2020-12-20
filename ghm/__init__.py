import logging
import os
import pathlib
import pygit2
import re


log = logging.getLogger(__name__)


def filter_repos(repos, owner_filter=None, repo_filter=None,
                 ignore_forks=False):
    if owner_filter:
        repos = [r for r in repos if re.search(owner_filter, r.owner.login)]
    if repo_filter:
        repos = [r for r in repos if re.search(repo_filter, r.name)]
    if ignore_forks:
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
    try:
        pygit2.clone_repository(
            url,
            path,
            callbacks=git_callbacks,
            bare=True,
            remote=git_mirror_remote
        )
    except ValueError:
        pass
    return True


# FIXME: Needs tests
def fetch_repo(path, git_callbacks=None, dry_run=False):
    repo = pygit2.Repository(path)
    remote = repo.remotes["origin"]
    log.info(f"Fetching: {remote.url} -> {path}")
    if dry_run:
        return False

    remote.fetch(callbacks=git_callbacks, prune=pygit2.GIT_FETCH_PRUNE)
    return True
