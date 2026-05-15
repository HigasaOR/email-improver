#!/bin/bash
set -e

# Add UV to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install UV if missing
if ! command -v uv &>/dev/null; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# Create venv with Python 3.13 on first run
if [ ! -d ".venv" ]; then
  echo "Setting up environment (first run)..."
  uv python install 3.13
  uv venv --python 3.13
  uv pip install -r requirements.txt
fi

# Launch
exec .venv/bin/python main.py
