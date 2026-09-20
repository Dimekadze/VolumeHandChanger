#!/usr/bin/env bash
set -e

REPO_URL="git@github.com:Dimekadze/VolumeHandChanger.git"
PROJECT_DIR="VolumeHandChanger"
PYTHON_VERSION="python3.12"
ENTRY_POINT="src/volumehandchanger/VolumeControl.py"

if ! command -v poetry &>/dev/null; then
    echo "Poetry not installed"
    exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
    git clone "$REPO_URL"
fi

cd "$PROJECT_DIR"

if ! poetry env list --full-path 2>/dev/null | grep -q .; then
    poetry env use "$PYTHON_VERSION" --no-interaction
    poetry install --no-interaction
fi

eval "$(poetry env activate)"
poetry run python "$ENTRY_POINT"
