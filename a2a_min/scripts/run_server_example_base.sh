#!/bin/bash -eu
set -o pipefail

#-----------------------------------------------------------------------------
#
# Run server example
#
#-----------------------------------------------------------------------------

# Get script directory
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPTS_DIR/config.sh"

# Activate virtual environment (with special handling for Windows)
echo "PROJECT_DIR;$PROJECT_DIR"
cd $PROJECT_DIR

# Go into the sub-dir (most projects don't need this)
cd $PROJECT_NAME

# Run the server
python $PROJECT_DIR/$PROJECT_NAME/examples/base/server_example.py
