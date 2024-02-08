# Contribution Guidelines
Thank you for your interest in contributing to shmessy.

## Prerequisites
Before you start, make sure you have **poetry** installed on your machine. You can install it with this command:

```bash
pip install poetry
```

Also, make sure you have **forked** the repository and **cloned** your fork to your local machine.

## Setup
To set up the project, navigate to the project directory and run these commands:

```bash
# Install the project dependencies
poetry install

# Install the pre-commit hooks
poetry run pre-commit install
```

## Testing and Linting
To run the tests, use this command:

```bash
poetry run pytest
```

To run the linter, use this command:

```bash
poetry run pylint src
```
