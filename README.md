# Github Mirrorer

Bulk mirror GitHub repositories

## Installation

    pip install ghm

## Running the Application

    ghm [options] <path>

Use `--help` to see available options.

## Development

### Getting Started

    pip install pipenv
    pipenv install --dev
    pipenv shell
    ...

### Running Tests

    pytest

### Releases

1. Bump `VERSION` in [ghm/meta.py](ghm/meta.py)
1. Update [CHANGELOG.md](CHANGELOG.md)
1. Run `make release`
