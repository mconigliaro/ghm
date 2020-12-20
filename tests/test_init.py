import os
import pygit2

import ghm


def test_filter_repos_owner(test_repos):
    repos = ghm.filter_repos(test_repos, owner="foo")
    names = [r.name for r in repos]
    assert names == ["baz", "qux"]


def test_filter_repos_repo(test_repos):
    repos = ghm.filter_repos(test_repos, repo="u")
    names = [r.name for r in repos]
    assert names == ["qux", "quux"]


def test_filter_repos_ignore_forks(test_repos):
    repos = ghm.filter_repos(test_repos, ignore_forks=True)
    names = [r.name for r in repos]
    assert names == ['baz', 'qux', 'quux']


def test_clone_path(tmp_path, ghm_repo):
    path = ghm.clone_path(tmp_path, ghm_repo)
    assert path == os.path.join(tmp_path, "mconigliaro", "ghm.git")


def test_mkdir_p(tmp_path):
    path = os.path.join(tmp_path, "foo", "bar", "baz")
    assert ghm.mkdir_p(path)
    assert os.path.exists(path)


def test_clone_repo_dry_run(ghm_repo, ghm_clone_path, git_credentials):
    assert not ghm.clone_repo(
        ghm_repo,
        ghm_clone_path,
        git_callbacks=git_credentials,
        dry_run=True
    )
    assert not os.path.exists(ghm_clone_path)


def test_clone_repo(ghm_repo, ghm_clone_path, git_credentials):
    repo = ghm.clone_repo(
        ghm_repo,
        ghm_clone_path,
        git_callbacks=git_credentials
    )
    assert repo.is_bare


def test_fetch_repo_dry_run(ghm_clone_path, git_credentials):
    assert not ghm.fetch_repo(
        ghm_clone_path,
        git_callbacks=git_credentials,
        dry_run=True
    )


def test_fetch_repo(ghm_clone_path, git_credentials):
    tp = ghm.fetch_repo(ghm_clone_path, git_callbacks=git_credentials)
    assert isinstance(tp, pygit2.remote.TransferProgress)
