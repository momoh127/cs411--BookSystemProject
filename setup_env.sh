#!/bin/bash

# how to run: check ls -l setup_env.sh if -rw-r--r-- then chmod +x setup_env.sh then ./setup_env.sh
# Set the name of the virtual environment directory
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"

# Check if the virtual environment already exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"

  # Activate the virtual environment
  source "$VENV_DIR/bin/activate"

  # Upgrade pip
  echo "Upgrading pip..."
  pip install --upgrade pip

  # Install dependencies from requirements.txt if it exists
  if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install --no-cache-dir -r "$REQUIREMENTS_FILE"
  else
    echo "Error: $REQUIREMENTS_FILE not found."
    exit 1
  fi
else
  echo "Virtual environment already exists. Activating..."
  source "$VENV_DIR/bin/activate"
fi

# Confirm activation and display environment info
echo "Virtual environment activated."
python --version
pip --version