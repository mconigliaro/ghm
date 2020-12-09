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
    return os.path.join(root, repo.owner.login, repo.name)


def mkdir_p(path, dry_run=False):
    if os.path.exists(path):
        return False
    log.debug(f"Creating directory: {path}")
    if dry_run:
        return False
    pathlib.Path(path).mkdir(parents=True)
    return True


# FIXME: Support other authentication methods (e.g. ssh key, user/pass)
def git_credentials_callback(token=None):
    credentials = pygit2.UserPass(token, "")
    return pygit2.RemoteCallbacks(credentials=credentials)


# FIXME: Support other URL types (e.g. ssh)
def clone_repo(repo, path, git_callbacks=None, dry_run=False):
    path = clone_path(path, repo)
    if os.path.isdir(path):
        log.debug(f"Skipping existing repository: {path}")
    else:
        mkdir_p(path, dry_run=dry_run)
        url = repo.clone_url
        log.info(f"Cloning: {url} -> {path}")
        if not dry_run:
            try:
                pygit2.clone_repository(url, path, callbacks=git_callbacks)
            except ValueError:
                pass
    return path

# FIXME: Implement git-pull
