import os
import pygit2

import ghm


def test_discover_token_notset():
    token = ghm.discover_token(envs=["TEST_TOKEN"])
    assert token.val is None


def test_discover_token():
    os.environ["TEST_TOKEN"] = "test"
    token = ghm.discover_token(envs=["TEST_TOKEN_NOTSET", "TEST_TOKEN"])
    del os.environ["TEST_TOKEN"]
    assert token.env == "TEST_TOKEN"
    assert token.val == "test"


def test_filter_repos_owner(test_repos):
    repos = ghm.filter_repos(test_repos, match_owner="foo")
    names = [r.name for r in repos]
    assert names == ["baz", "qux"]


def test_filter_repos_repo(test_repos):
    repos = ghm.filter_repos(test_repos, match_repo="u")
    names = [r.name for r in repos]
    assert names == ["qux", "quux"]


def test_filter_repos_exclude_owner(test_repos):
    repos = ghm.filter_repos(test_repos, exclude_owner="foo")
    names = [r.name for r in repos]
    assert names == ['quux', 'corge']


def test_filter_repos_exclude_repo(test_repos):
    repos = ghm.filter_repos(test_repos, exclude_repo="u")
    names = [r.name for r in repos]
    assert names == ['baz', 'corge']


def test_filter_repos_exclude_forks(test_repos):
    repos = ghm.filter_repos(test_repos, exclude_forks=True)
    names = [r.name for r in repos]
    assert names == ['baz', 'qux', 'quux']


def test_clone_path(tmp_path, ghm_repo):
    path = ghm.clone_path(tmp_path, ghm_repo)
    assert path == os.path.join(tmp_path, "mconigliaro", "ghm.git")


def test_mkdir_p(tmp_path):
    path = os.path.join(tmp_path, "foo", "bar", "baz")
    assert ghm.mkdir_p(path)
    assert os.path.exists(path)


def test_clone_repo_dry_run(ghm_repo, ghm_clone_path):
    assert not ghm.clone_repo(
        ghm_repo,
        ghm_clone_path,
        dry_run=True
    )
    assert not os.path.exists(ghm_clone_path)


def test_clone_repo(ghm_repo, ghm_clone_path):
    repo = ghm.clone_repo(
        ghm_repo,
        ghm_clone_path
    )
    assert repo.is_bare


def test_fetch_repo_dry_run(ghm_clone_path):
    assert not ghm.fetch_repo(
        ghm_clone_path,
        dry_run=True
    )


def test_fetch_repo(ghm_clone_path):
    tp = ghm.fetch_repo(ghm_clone_path)
    assert isinstance(tp, pygit2.remote.TransferProgress)
