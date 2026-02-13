import src.api as api
from pprint import pprint
import urllib.parse
import json

def show_current_user():
    try:
        data = api.get("/me")
        print("Aktueller Benutzer:")
        for key, val in data.items():
            print(f"  {key}: {val}")
    except Exception as e:
        print(f"Fehler beim Abruf: {e}")

def show_user_details_by_username(username: str):
    try:
        endpoint = "/user/search?username=" + urllib.parse.quote(username)
        data = api.get(endpoint)

        if not isinstance(data, dict):
            print("Unerwartetes Antwortformat.")
            return

        print("Benutzerdetails:")
        print(f"  ID        : {data.get('userId', '?')}")
        print(f"  Username  : {data.get('username', '?')}")
        print(f"  Enabled   : {data.get('isEnabled', '?')}")
        print(f"  Last Auth : {data.get('lastAuth', '?')}")
        print(f"  Companies : {data.get('companies', [])}")

    except Exception as e:
        print(f"Fehler beim Abrufen der Benutzerdetails: {e}")

from src.api import call_api_generic

def set_user_rights(company_id: int, username: str, level: str):
    """
    Setzt den Benutzerlevel (USER, ADMIN, READ_ONLY) eines Benutzers in einer Company.
    Beispiel: dpms_call rights 5474 thorsten.dombach@gmail.com USER
    """
    allowed_levels = ["USER", "ADMIN", "READ_ONLY", "CUSTOM"]
    if level.upper() not in allowed_levels:
        print(f"[Fehler] Ungültiger Level '{level}'. Erlaubt sind: {', '.join(allowed_levels)}")
        return

    endpoint = f"/company/{company_id}/user"
    body = {
        "username": username,
        "useSso": False,
        "level": level.upper(),
        "levelId": None
    }

    print(f"[INFO] Setze Rechte für {username} in Company {company_id} auf Level {level.upper()}...")
    try:
        # Verwende call_api_generic direkt mit POST
        api.call_api_generic("POST", endpoint, json.dumps(body))
    except Exception as e:
        print(f"[Fehler] Änderung der Benutzerrechte fehlgeschlagen: {e}")
        