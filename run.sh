#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Error: .venv not found at $VENV_DIR"
    exit 1
fi

if [ -z "$VIRTUAL_ENV" ]; then
    source "$VENV_DIR/bin/activate"
fi

streamlit run "$SCRIPT_DIR/app.py"
