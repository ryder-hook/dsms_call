from src.api import get

def list_company_users(company_id: int):
    """
    Gibt alle Benutzer einer Company aus – inklusive Benutzername, Level, Level-ID und Level-Name.
    """
    try:
        # Lade alle Level-Bezeichner (Mapping levelId → name)
        level_data = get("/levels")
        level_map = {}

        if isinstance(level_data, list):
            for entry in level_data:
                level_id = entry.get("levelId")
                name = entry.get("name", "")
                if level_id is not None:
                    level_map[int(level_id)] = name  # levelId sicher als int

        # Lade Company-Daten inkl. Benutzerliste
        endpoint = f"/company/{company_id}"
        data = get(endpoint)

        if "users" not in data or not isinstance(data["users"], list):
            print(f"[Fehler] Keine Benutzer für Company {company_id} gefunden.")
            return

        print(f"Benutzer der Company {company_id}:")
        print("  ID  | Username                         | Level     | Level-ID | Level-Name")
        print("------|----------------------------------|-----------|----------|----------------")

        for user in data["users"]:
            uid = str(user.get("userId", "?")).rjust(5)
            uname = user.get("username", "?").ljust(32)
            lvl = user.get("level", "?").ljust(9)

            lvlid_raw = user.get("levelId", None)
            if isinstance(lvlid_raw, int):
                lvlid = str(lvlid_raw)
                lvlname = level_map.get(lvlid_raw, "")  # Zugriff über int-Key
            else:
                lvlid = ""
                lvlname = ""

            print(f"{uid} | {uname} | {lvl} | {lvlid.ljust(8)} | {lvlname}")

    except Exception as e:
        print(f"[Fehler] Konnte Benutzerliste nicht abrufen: {e}")