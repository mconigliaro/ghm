import os

import ghm


def test_filter_repos_owner_filter(test_repos):
    repos = ghm.filter_repos(test_repos, owner_filter="foo")
    names = [r.name for r in repos]
    assert names == ["baz", "qux"]


def test_filter_repos_repo_filter(test_repos):
    repos = ghm.filter_repos(test_repos, repo_filter="u")
    names = [r.name for r in repos]
    assert names == ["qux", "quux"]


def test_filter_repos_ignore_forks(test_repos):
    repos = ghm.filter_repos(test_repos, ignore_forks=True)
    names = [r.name for r in repos]
    assert names == ['baz', 'qux', 'quux']


def test_clone_path(tmp_path, ghm_repo):
    path = ghm.clone_path(tmp_path, ghm_repo)
    assert path == os.path.join(tmp_path, "mconigliaro", "ghm")


def test_mkdir_p_dry_run(tmp_path):
    path = os.path.join(tmp_path, "foo", "bar", "baz")
    assert not ghm.mkdir_p(path, dry_run=True)
    assert not os.path.exists(path)


def test_mkdir_p(tmp_path):
    path = os.path.join(tmp_path, "foo", "bar", "baz")
    assert ghm.mkdir_p(path)
    assert os.path.exists(path)


def test_clone_repo_dry_run(ghm_repo, tmp_path, token):
    path = ghm.clone_repo(ghm_repo, tmp_path, token=token, dry_run=True)
    assert not os.path.exists(os.path.join(path, ".git"))


def test_clone_repo(ghm_repo, tmp_path, token):
    path = ghm.clone_repo(ghm_repo, tmp_path, token=token)
    assert os.path.exists(os.path.join(path, ".git"))
