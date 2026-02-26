#!/bin/bash

set -e

function cleanup {
    exit $?
}

trap "cleanup" EXIT

# Check black code style
black --check .

# Check PEP-8 code style and McCabe complexity
flake8 . --count --show-source --statistics

# run tests with test coverage
pytest tests/
