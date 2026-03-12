#!/bin/bash

# Absolute Pfade ermitteln
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"

# Virtuelle Umgebung verwenden, wenn vorhanden
SCRIPT_NAME="$(basename "$PROJECT_DIR")"
VENV_PY="$HOME/.local/venvs/$SCRIPT_NAME/bin/python"

if [ -x "$VENV_PY" ]; then
  PYTHON="$VENV_PY"
else
  PYTHON="$(which python3)"
fi

# Setze PYTHONPATH auf das Projektverzeichnis (damit src/ gefunden wird)
export PYTHONPATH="$PROJECT_DIR"

# Starte das Modul im Paketkontext
exec "$PYTHON" -m src.main "$@"