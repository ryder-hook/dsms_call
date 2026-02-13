import os
import sys

def load_token(token_path: str) -> str:
    try:
        with open(os.path.expanduser(token_path), "r", encoding="utf-8") as f:
            token = f.read().strip()
            if not token:
                sys.exit("[Fehler] Token-Datei ist leer.")
            return token
    except FileNotFoundError:
        sys.exit(f"[Fehler] Token-Datei nicht gefunden unter {token_path}")
    except Exception as e:
        sys.exit(f"[Fehler] Fehler beim Laden des Tokens: {e}")