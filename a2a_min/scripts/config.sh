#-----------------------------------------------------------------------------
#
# This script sets up the environment for the project by defining the
# project directory and activating the virtual environment.
#
#-----------------------------------------------------------------------------

export SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Project directory
export PROJECT_DIR="$( cd $SCRIPTS_DIR/../.. && pwd -P )"
export PROJECT_NAME="$(basename $PROJECT_DIR)"

# Data directories
export DATA_DIR="$PROJECT_DIR/data"
export LOGS_DIR="$PROJECT_DIR/logs"
export PG_DATA_DIR="$DATA_DIR/data/db/postgres"

# Server configuration
export PORT=8081

# Activate virtual environment
if [ "${OS-}" == "Windows_NT" ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

