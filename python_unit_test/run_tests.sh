#!/bin/bash

# export PYTHONPATH="/home/harismallick/Documents/general_scripts/python_unit_test:$PYTHONPATH"

directory="./tests/src" # Replace with the actual directory path

# Check if the directory exists
if [ ! -d "$directory" ]; then
  echo "Error: Directory '$directory' not found."
  exit 1
fi

# Iterate through all files in the directory
for file in "$directory"/*; do
  # Check if the current item is a regular file
  if [ -f "$file" ]; then
    # Execute the Python file using the python interpreter
    echo "Executing: $file"
    python3 "$file" # or python "$file", depending on your system's python version.
    if [ $? -ne 0 ]; then
        echo "Error: $file failed to execute."
    fi
  fi
done

exit 0