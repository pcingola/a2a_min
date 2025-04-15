#!/bin/bash -eu
set -o pipefail


# Get script directory
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPTS_DIR/config.sh"

# Run linter
ruff check . \
    --exclude notebooks \
    --exclude data \
    --exclude .env \
    --ignore F403 \
    --fix \
