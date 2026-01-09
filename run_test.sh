#!/bin/bash

echo "Running Simulation Test..."

# URL default
URL="http://localhost:8000/simulate"

# Run the python script
if [ -f "src/scripts/manual_trigger.py" ]; then
    python3 src/scripts/manual_trigger.py --url "$URL" "$@"
    
    if [ $? -eq 0 ]; then
        echo "Test script executed successfully."
    else
        echo "Test script failed."
    fi
else
    echo "Error: src/manual_trigger.py not found!"
fi
