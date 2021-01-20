import os
import pytest
from github.Repository import Repository

import ghm


@pytest.fixture
def test_repos():
    attrs = [
        {"owner": "foo", "name": "baz", "fork": False},
        {"owner": "foo", "name": "qux", "fork": False},
        {"owner": "bar", "name": "quux", "fork": False},
        {"owner": "bar", "name": "corge", "fork": True},
    ]

    return [
        Repository(
            None,
            None,
            {
                "full_name": f"{a['owner']}/{a['name']}",
                "owner": {"login": a["owner"]},
                "name": a["name"],
                "fork": a["fork"]
            },
            None)
        for a in attrs
    ]


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
