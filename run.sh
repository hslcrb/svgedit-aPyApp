#!/bin/bash
# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -f "app/venv/bin/activate" ]; then
    source app/venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Run the application
# Use PYTHONPATH to ensure imports work if necessary, though simple execution often suffices
export PYTHONPATH=$PYTHONPATH:$SCRIPT_DIR/app

python3 app/main.py "$@"
