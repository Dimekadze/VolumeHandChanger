#!/usr/bin/env bash
set -e

PYTHON_VERSION="python3.12"
ENTRY_POINT="src/volumehandchanger/VolumeControl.py"

if ! command -v poetry &>/dev/null; then
    echo "Poetry not installed"
    exit 1
fi

if ! poetry env list --full-path 2>/dev/null | grep -q .; then
    poetry env use "$PYTHON_VERSION" --no-interaction
    poetry install --no-interaction
fi

eval "$(poetry env activate)"
poetry run python "$ENTRY_POINT"
