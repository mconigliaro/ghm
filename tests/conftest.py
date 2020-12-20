import os
import pytest
from github.Repository import Repository

import ghm


@pytest.fixture
def test_repos():
    attrs = [
        {"name": "baz", "owner": {"login": "foo"}, "fork": False},
        {"name": "qux", "owner": {"login": "foo"}, "fork": False},
        {"name": "quux", "owner": {"login": "bar"}, "fork": False},
        {"name": "corge", "owner": {"login": "bar"}, "fork": True}
    ]
    return [Repository(None, None, a, None) for a in attrs]


@pytest.fixture(scope='session')
def ghm_repo():
    return Repository(
        None,
        None,
        {
            "name": "ghm",
            "owner": {
                "login": "mconigliaro"
            },
            "clone_url": "https://github.com/mconigliaro/ghm.git"
        },
        None
    )


@pytest.fixture(scope='session')
def ghm_clone_path(tmp_path_factory, ghm_repo):
    return ghm.clone_path(tmp_path_factory.getbasetemp(), ghm_repo)


@pytest.fixture
def git_credentials():
    token = os.environ.get("GH_TOKEN")
    return ghm.git_credentials_callback(token=token)
