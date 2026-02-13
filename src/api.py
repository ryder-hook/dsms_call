import urllib.parse
import sys
import json
import requests
from src.config import load_config


def get(endpoint: str) -> dict:
    config = load_config()
    url = config["base_url"].rstrip("/") + config["api_prefix"] + "/" + endpoint.lstrip("/")
    token_path = config["token_path"]

    try:
        with open(token_path, "r", encoding="utf-8") as f:
            token = f.read().strip()
    except FileNotFoundError:
        raise RuntimeError(f"Token-Datei nicht gefunden: {token_path}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API-Fehler: {e}")


def call_api(base_url: str, endpoint: str, token: str) -> dict:
    config = load_config()
    api_prefix = config["api_prefix"]
    full_base = base_url.rstrip("/") + api_prefix

    url = urllib.parse.urljoin(full_base + "/", endpoint.lstrip("/"))
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        sys.exit(f"[Fehler] API-Fehler: {e}")
    except Exception as e:
        sys.exit(f"[Fehler] Verbindungsfehler: {e}")


def call_api_generic(method: str, endpoint: str, body: str = None):
    """
    Führt einen beliebigen HTTP-Aufruf (GET, POST, PUT, DELETE) gegen die DSMS-API aus.
    Beispiel:
      dpms_call gen get /user/search?username=test@example.com
      dpms_call gen post /company/4711/user '{"username":"api@example.com","level":"ADMIN"}'
    """
    config = load_config()
    url = config["base_url"].rstrip("/") + config["api_prefix"] + "/" + endpoint.lstrip("/")
    token_path = config["token_path"]

    try:
        with open(token_path, "r", encoding="utf-8") as f:
            token = f.read().strip()
    except FileNotFoundError:
        raise RuntimeError(f"Token-Datei nicht gefunden: {token_path}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    json_body = None
    if body:
        try:
            json_body = json.loads(body)
        except json.JSONDecodeError:
            sys.exit("[Fehler] Ungültiger JSON-Body – bitte korrektes JSON angeben.")

    try:
        response = requests.request(method.upper(), url, headers=headers, json=json_body, timeout=15)
        response.raise_for_status()
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except ValueError:
            print(response.text)
    except requests.exceptions.RequestException as e:
        sys.exit(f"[Fehler] API-Fehler: {e}")