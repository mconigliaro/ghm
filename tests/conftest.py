import os
import pytest

from github.Repository import Repository


@pytest.fixture
def test_repos():
    attrs = [
        {"name": "baz", "owner": {"login": "foo"}},
        {"name": "qux", "owner": {"login": "foo"}},
        {"name": "quux", "owner": {"login": "bar"}},
        {"name": "corge", "owner": {"login": "bar"}}
    ]
    return [Repository(None, None, a, None) for a in attrs]


@pytest.fixture
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


@pytest.fixture
def token():
    return os.environ.get("GH_TOKEN")
