#!/usr/bin/env python3
# --- Mabunta Python Bootstrap ---
# Nutzt bevorzugt .venv/bin/python im Projektordner, prüft Mindestversion

import os
import sys
import json

MIN_VER = (3, 10)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME = os.path.basename(os.path.dirname(PROJECT_DIR))
VENV_DIR = os.path.join(os.path.expanduser("~"), ".local", "venvs", SCRIPT_NAME)
VENV_PY = os.path.join(VENV_DIR, "bin", "python")


def _same_exec(a, b):
    try:
        return os.path.realpath(a) == os.path.realpath(b)
    except Exception:
        return a == b


# 1) Virtuelle Umgebung aus .venv bevorzugen, falls vorhanden und nicht aktiv
if (
    os.path.exists(VENV_PY)
    and os.access(VENV_PY, os.X_OK)
    and not _same_exec(VENV_PY, sys.executable)
):
    os.execv(VENV_PY, [VENV_PY] + sys.argv)


# 2) Mindestversion prüfen, ggf. alternative Python-Binärdateien probieren
if sys.version_info < MIN_VER:
    candidates = [
        "/opt/homebrew/bin/python3",
        "/usr/local/bin/python3",
        "/opt/local/bin/python3",
    ]
    os.environ["PATH"] = (
        "/opt/homebrew/bin:/usr/local/bin:/opt/local/bin:"
        + os.environ.get("PATH", "")
    )
    for py in candidates:
        if os.path.exists(py) and os.access(py, os.X_OK) and not _same_exec(py, sys.executable):
            os.execv(py, [py] + sys.argv)
    sys.stderr.write(
        f"Warnung: Python {sys.version.split()[0]} < {MIN_VER[0]}.{MIN_VER[1]} – keine neuere Python gefunden. Weiter mit aktueller Umgebung.\n"
    )


# --- Pfad anpassen, damit Imports funktionieren ---
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# --- DSMS CLI-Funktionen ---
import src.config as config
import src.auth as auth
import src.api as api
import src.user as user
import src.company as company


def show_help():
    print("""
DSMS Command Line Interface – mehr Details, siehe: https://docs.dpms-online.de
Verfügbare Befehle:

  dpms_call.sh me
      → Zeigt die Daten des aktuellen Benutzers.
      Beispiel: dpms_call.sh me

  dpms_call.sh companies
      → Listet alle Companies auf.
      Beispiel: dpms_call.sh companies

  dpms_call.sh company <ID>
      → Zeigt alle Benutzer einer Company – inklusive Level, Level-ID und Level-Name (falls vorhanden).
      Beispiel: dpms_call.sh company 5474

  dpms_call.sh user <E-Mail>
      → Zeigt Details zu einem Benutzer (z. B. Status, letzte Anmeldung).
      Beispiel: dpms_call.sh user stefan.test@domain.de

  dpms_call.sh rights <Company-ID> <E-Mail> <Level>
      → Ändert den Benutzerlevel (USER, ADMIN, READ_ONLY) für eine Company.
      Beispiel: dpms_call.sh rights 4711 stefan.test@domain.de READ_ONLY

  dpms_call.sh gen <METHOD> <ENDPOINT> [JSON]
      → Führt einen generischen API-Aufruf aus (GET, POST, PUT, DELETE).
      Beispiel GET:  dpms_call.sh gen get "/user/search?username=stefan.test@domain.de"
      Beispiel POST: dpms_call.sh gen post "/company/5474/user" '{"username":"api@example.com","useSso":false,"level":"USER"}'

  dpms_call.sh help
      → Zeigt diese Hilfe an.
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    command = sys.argv[1].lower()

    # Hilfe direkt anzeigen
    if command in ("help", "-h", "--help"):
        show_help()
        sys.exit(0)

    cfg = config.load_config()
    token = auth.load_token(cfg["token_path"])

    # ---------------------------------------------------
    # 1) Benutzerinfo
    # ---------------------------------------------------
    if command == "me":
        user.show_current_user()

    # ---------------------------------------------------
    # 2) Companies anzeigen
    # ---------------------------------------------------
    elif command == "companies":
        company.list_companies()

    # ---------------------------------------------------
    # 3) Benutzer einer Company anzeigen
    # ---------------------------------------------------
    elif command == "company":
        if len(sys.argv) < 3:
            print("Fehlender Parameter: Company-ID.")
            sys.exit(1)
        try:
            cid = int(sys.argv[2])
            company.list_company_users(cid)
        except ValueError:
            print("Company-ID muss eine Zahl sein.")
            sys.exit(1)

    # ---------------------------------------------------
    # 4) Details eines Benutzers
    # ---------------------------------------------------
    elif command == "user":
        if len(sys.argv) < 3:
            print("Fehlender Parameter: Benutzername (E-Mail).")
            sys.exit(1)
        username = sys.argv[2]
        user.show_user_details_by_username(username)

    # ---------------------------------------------------
    # 5) Rechte eines Benutzers ändern
    # ---------------------------------------------------
    elif command == "rights":
        if len(sys.argv) < 5:
            print("Verwendung: dpms_call rights <Company-ID> <E-Mail> <Level>")
            sys.exit(1)
        company_id = sys.argv[2]
        username = sys.argv[3]
        level = sys.argv[4]
        user.set_user_rights(company_id, username, level)

    # ---------------------------------------------------
    # 6) Generischer API-Aufruf
    # ---------------------------------------------------
    elif command == "gen":
        if len(sys.argv) < 4:
            print("Verwendung: dpms_call.sh gen [GET|POST|PUT|DELETE] <endpoint> [json-body]")
            sys.exit(1)

        method = sys.argv[2].upper()
        endpoint = sys.argv[3]
        json_input = sys.argv[4] if len(sys.argv) > 4 else None

        try:
            api.call_api_generic(method, endpoint, json_input)
        except Exception as e:
            print(f"[Fehler] API-Aufruf fehlgeschlagen: {e}")
            sys.exit(1)

    # ---------------------------------------------------
    # Unbekannter Befehl
    # ---------------------------------------------------
    else:
        print(f"Unbekannter Befehl: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()