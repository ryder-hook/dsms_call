import os
import json
import sys

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        # Pflichtfelder prüfen
        base_url = cfg.get("base_url", "").rstrip("/")
        if not base_url:
            sys.exit("[Fehler] base_url fehlt in config.json")

        token_path_raw = cfg.get("token_path")
        if not token_path_raw:
            sys.exit("[Fehler] token_path fehlt in config.json")

        token_path = os.path.expanduser(token_path_raw)

        # Optionaler oder definierter API-Prefix
        api_prefix = cfg.get("api_prefix", "/api/v1").rstrip("/")

        return {
            "base_url": base_url,
            "token_path": token_path,
            "api_prefix": api_prefix,
        }

    except FileNotFoundError:
        sys.exit(f"[Fehler] Konfigurationsdatei {config_path} nicht gefunden.")
    except json.JSONDecodeError:
        sys.exit("[Fehler] config.json enthält ungültiges JSON.")
    except Exception as e:
        sys.exit(f"[Fehler] Fehler beim Laden der Konfiguration: {e}")