# Github Mirrorer

Easily mirror GitHub repositories

## Installation

    pip install ghm

## Running the Application

    ghm [options] <path>

Your GitHub personal access token will automatically be read from either the `GH_TOKEN` or `GITHUB_TOKEN` environment variable (whichever is set). When this is the case, ghm will mirror all your personal repositories, as well as every repository from every organization your account belongs to.

When not using authentication, you can mirror a user or organization's public repositories by using the `--user` or `--org` options respectively.

Use `--help` to see available options.

## Development

### Getting Started

    pip install pipenv
    pipenv install --dev
    pipenv shell
    ...

### Running Tests

    pytest
