# Github Mirrorer

[![Continuous Integration](https://github.com/mconigliaro/ghm/actions/workflows/ci.yml/badge.svg)](https://github.com/mconigliaro/ghm/actions/workflows/ci.yml)

Simple command-line utility for bulk mirroring GitHub repositories

## Features

- Discover repositories by username or organization
- Use regular expressions to filter by repository name or owner
- Exclude forks
- Mirror several repositories in parallel
- Dry-run mode (shows what will happen without mirroring anything)

## Installation

    pip install ghm

## Running the Application

    ghm [options] <path>

Use `--help` to see available options.

## Development

### Getting Started

    poetry install
    poetry shell
    ...

### Running Tests

    pytest

### Releases

1. Bump `version` in [pyproject.toml](pyproject.toml)
1. Update [CHANGELOG.md](CHANGELOG.md)
1. Run `make release`
