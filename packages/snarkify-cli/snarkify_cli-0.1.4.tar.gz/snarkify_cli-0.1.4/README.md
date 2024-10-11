# Snarkify CLI

The command line utility to interact with the Snarkify platform.

## Dev Installation
1. Install [poetry](https://python-poetry.org/)
2. Run `poetry install` in the root directory
3. Run `poetry shell` to get access to `snarkify` command

## Build and install CLI
```
poetry build
# Note the the version of the CLI is subject to change.
pip3 install dist/snarkify_cli-0.1.0-py3-none-any.whl
pip3 uninstall dist/snarkify_cli-0.1.0-py3-none-any.whl
```

## Run tests
```
poetry run pytest
```