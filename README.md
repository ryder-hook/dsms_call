# DSMS API Tool

Ein plattformübergreifendes Kommandozeilen-Tool zur Anbindung an die REST-API eines White-Label-DSMS-Systems.

## Zielgruppe

Diese Anleitung richtet sich an technisch versierte Nutzer (z. B. IT-Administratoren oder Informationssicherheitsbeauftragte), die keine Python-Kenntnisse besitzen, aber mit Kommandozeile, Visual Studio Code und Dateisystemen unter Windows oder macOS umgehen können.

## Funktionen

- Auflisten von Mandanten (Companies)
- Anzeige von Benutzerstatus und Schulungsdaten
- Aktivieren oder Sperren von Benutzern je Mandant
- (optional) Aktivieren/Deaktivieren einzelner Mandantenfunktionen (z. B. Whistleblower-Modul)
- Erweiterbar durch modulare Struktur

## Voraussetzungen

| Komponente        | macOS                         | Windows                        |
|-------------------|-------------------------------|--------------------------------|
| Python            | vorinstalliert (ab 3.8)       | https://www.python.org         |
| Terminal          | ZSH (Standard)                | PowerShell oder CMD            |
| Visual Studio Code| empfohlen                     | empfohlen                      |

## Installation

### API-Token einrichten

- Login auf dem DPMS als entsprechender User
- Unter PRofilverwaltung -> Rest-Schnittstelle ein API-Token generieren
- Achtung Benutzer muss entsprechende Rechte haben, um alle Befehle ausführen zu können
- Token-Datei erstellen, siehe unten

### macOS

#### Environment erstellen

```bash
cd ~/Documents
git clone <Projekt-Repository> dsms
cd dsms
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Token Datei erstellen

```bash
mkdir -p ~/.config/dsms_api
nano ~/.config/dsms_api/token
chmod 600 ~/.config/dsms_api/token
```
### Windows (PowerShell)

#### Environment erstellen
```bash
cd $HOME\Documents
# Projektordner entpacken oder klonen
cd dsms
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```
#### Token Datei erstellen

Die Datei muss ausschließlich den Token enthalten, ohne Anführungszeichen oder Leerzeilen.
```bash
%USERPROFILE%\.config\dsms_api\token
```
## Test der Installation

### Manuelle Testausführung

Nach der Einrichtung kannst du die Funktionalität des Skripts direkt testen. Verwende dazu den `me`-Aufruf, um zu prüfen, ob:

- die Python-Umgebung korrekt geladen wird
- die `config.json` erfolgreich gelesen wird
- die Verbindung zum Server funktioniert
- das Auth-Token gültig ist

#### Test unter macOS (Terminal)

```zsh
cd ~/Documents/dsms
python3 -m src.main me
```
#### Test unter Windows
```bash
cd %USERPROFILE%\Documents\dsms
python3 -m src.main me
```
### Erwartete Ausgabe

Bei korrekter Konfiguration wird ein JSON-Objekt mit den Informationen über den aktuell authentifizierten Benutzer angezeigt, z. B.:
{"username":"stefan.testh@domain.de","systemLang":"DE","email":"stefan.test@domain.de"}