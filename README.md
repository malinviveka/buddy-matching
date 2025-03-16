# Buddy-Matching
Repository für das Matching-Software-Projekt für den ISS

## Installation und Setup des Projekts

Diese Anleitung beschreibt die Schritte, um das Projekt auf einem lokalen Rechner einzurichten.

### 1. PostgreSQL installieren
- PostgreSQL kann unter [PostgreSQL - Download](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) heruntergeladen werden.
- Während des Installationsprozesses muss ein Passwort festgelegt werden. Es wird empfohlen, das Passwort gut zu speichern, da es später benötigt wird.
- Der Standardport 5432 sollte beibehalten werden.
- Der Installationsprozess kann anschließend fortgesetzt werden.

### 2. Repository klonen
- Git kann unter [Git - Download](https://git-scm.com/downloads) heruntergeladen werden.
- Eine bevorzugte IDE, wie z.B. Visual Studio Code, kann unter [Download-Link](https://code.visualstudio.com/download) heruntergeladen und geöffnet werden.
- Im Terminal sollte überprüft werden, ob Git korrekt in der Umgebungsvariable `PATH` konfiguriert ist. Hierzu kann der folgende Befehl ausgeführt werden:
   ```bash
   git --version
   ```
   Falls eine Fehlermeldung erscheint, sind folgende Schritte erforderlich:
    - Zu Systemsteuerung > System > Erweiterte Systemeinstellungen > Umgebungsvariablen navigieren.
    - In den Systemvariablen nach PATH suchen, es bearbeiten und folgenden Pfad hinzufügen:
      ```bash
      C:\Program Files\Git\bin
      ```
    - Visual Studio Code neu starten und das Terminal erneut öffnen. Es sollte dann erneut überprüft werden:
      ```bash
      git --version
      ```
- Zu dem Ordner navigieren, in dem das Repository gespeichert werden soll:
  ```bash
  cd /pfad/zum/zielordner
  ```
- Das Repository mit dem folgenden Befehl klonen:
  ```bash
  git clone https://github.com/malinviveka/buddy-matching.git
  ```
- Das Projekt kann anschließend über open folder in der IDE geöffnet werden.


### 3. Virtuelle Umgebung erstellen
- Eine virtuelle Umgebung kann mit folgendem Befehl erstellt werden:
  
  WINDOWS:
  ```bash
  python -m venv venv
  ```
  MAC:
  ```bash
  python3 -m venv venv
  ```
- Die virtuelle Umgebung wird mit folgendem Befehl aktiviert:
  
  WINDOWS:
  ```bash
  ./venv/scripts/activate
  ```
  MAC:
  ```bash
  source ./venv/bin/activate
  ``
  Sollte dabei ein Fehler auftreten, kann der folgende Befehl ausgeführt werden, um die PowerShell-Skriptausführungsrichtlinie anzupassen:
  ```bash
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  ```
- Die benötigten Abhängigkeiten können mit folgendem Befehl installiert werden:
  
  WINDOWS:
  ```bash
  py -m pip install -r requirements.txt
  ```
  MAC:
  ```bash
  python3 -m pip install -r requirements.txt
  ``

### 4. Datenbank anlegen
- Es kann überprüft werden, ob psql korrekt installiert wurde, indem der folgende Befehl ausgeführt wird:
  ```bash
  psql --version
  ```
- Sollte eine Fehlermeldung erscheinen, sind folgende Schritte erforderlich:
  - Zu Systemsteuerung > System > Erweiterte Systemeinstellungen > Umgebungsvariablen navigieren.
  - In den Systemvariablen nach PATH suchen, es bearbeiten und folgenden Pfad hinzufügen (ersetze VERSION mit der installierten Version von PostgreSQL):
    ```bash
    C:\Program Files\PostgreSQL\VERSION\bin
    ```
  - Visual Studio Code neu starten und das Terminal erneut öffnen. Es sollte dann erneut überprüft werden:
    ```bash
    psql --version
    ```
- Eine Verbindung zum PostgreSQL-Server wird mit folgendem Befehl hergestellt:
  ```bash
  psql -U postgres
  ```
- Es wird nach dem Passwort gefragt, das während der Installation von PostgreSQL festgelegt wurde.
- Die Datenbank und der Benutzer können mit den folgenden Befehlen erstellt werden:
  ```sql
  CREATE DATABASE buddymatchingdatabase;
  CREATE USER buddymatchinguser WITH PASSWORD 'P455w0rd';
  GRANT ALL PRIVILEGES ON DATABASE buddymatchingdatabase TO buddymatchinguser;
  ```
- Die psql-Session wird mit folgendem Befehl beendet:
  ```bash
  \q
  ```


### 5. Migration ausführen
Die Migrationen, um die Datenbankstruktur zu erstellen, können mit den folgenden Befehlen ausgeführt werden:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Übersetzung der Website
Übersetzungen, die im Code als solche markiert wurden, können über folgende Befehle in der entprechenden Datei erstellt und kompliliert werden: 
```bash
python manage.py makemessages -l de -l en
python manage.py compilemessages
```
### 7. Mobile Viewports
Die Adminansicht ist nicht optimiert für Mobile Devices!



---


## Docker
Für die Entwicklung kann [Docker](https://docs.docker.com/get-started/) genutzt werden, um die Datenbank leichter zu verwalten.
Hierfür kann eine `docker-compose.yml` im Verzeichnis angelegt werden, die beschreibt, wie der Postgres Container konfiguriert wird.

```yml
version: '3.8'

services:
  postgres:
    image: postgres:latest
    container_name: postgres_server
    environment:
      POSTGRES_USER: buddymatchinguser
      POSTGRES_PASSWORD: P455w0rd
      POSTGRES_DB: buddymatchingdatabase
    ports:
      - "5433:5432"

```

Der Container kann dann über `docker compose up` (im selben Verzeichnis wie die ``docker-compose.yml``) gestartet werden, optional auch als `docker compose up -d` um sich nicht an die Datenbanklogs anzuhängen.
Um den Container zu stoppen kann `docker compose down` verwendet werden. Insbesondere lassen sich alle Daten der Datenbank über `docker compose down -v` löschen. Dieser Befehl kann auch ausgeführt werden, wenn der Container nicht läuft.

Zu beachten ist zusätzlich, dass jedes Mal `python manage.py migrate` ausgeführt werden muss, wenn die Datenbank neu initalisiert wurde.
Zusätzlich ist der Port gerade auf `5433` eingestellt, damit er sich nicht mit möglichen existierenden Datenbanken schneidet. Damit also diese Datenbank verwendet wird, muss auch in den `settings.py` der `PORT` unter `DATABASE` auf `5433` gestellt werden. 

- - - 

Um Typescript Dateien in JavaScript zu kompilieren, kann über das Terminal der Befehl `tsc` ausgeführt werden. Durch diesen werden die Typescript files dann in Javascript "übersetzt".

- - - 
## Continuous Integration

Unser Projekt verwendet GitHub Actions für die **Continuous Integration (CI)**, um die Qualität und Wartbarkeit des Codes zu gewährleisten. Die CI-Pipeline läuft automatisch bei jeder Push- und Pull-Anfrage an den main-Branch.

### Was wird von CI geprüft? (`ci.yaml`)
- Check Python code formatting & Lints (ruff): überprüft Python Formatierungs- und Linting-Fehler
- Check Django template formatting (djlint): sorgt für konsistente Formatierung in Django-Templates
- Check JavaScript & CSS formatting (Prettier): stellt sicher, dass JavaScript- und CSS-Dateien der Standardformatierung folgen
- Django Migrations & Tests: Führt Datenbankmigrationen durch und führt Django-Tests aus, um die Funktionalität sicherzustellen
	- Hierbei sind in der CI Files alle Test-Dateien aus den verschiedenen Apps aufgelistet, um sicherzustellen, dass alle Tests ausgeführt werden. Sollten weitere Test-Files hinzugefügt werden, sollten diese hier ebenfalls ergänzt werden.

## Automatische Formattierung (`auto-format.yml`)
In dieser CI-Workflow-Konfiguration wurde eine automatisierte Formatierung implementiert, die auf das Kommando `/format` in Pull-Request-Kommentaren reagiert. Wenn dieses Kommando ausgelöst wird, passiert folgendes:
- Prüfung des betroffenen Pull-Request-Branch
- Installation der erforderlichen Abhängigkeiten (einschließlich Python-Tools wie Ruff und Djlint sowie das JavaScript-Tool Prettier) 
- Ausführung der Code-Formattierung 
- Prüfung nach Änderungen -> sollten Änderungen vorgenommen sein, werden diese automatisch committet und in das Repository gepusht
Diese Automatisierung stellt sicher, dass der Code immer einheitlich und nach den definierten Konventionen formatiert ist, ohne manuelle Eingriffe.

- - - 
## Zukünftige Erweiterung
Für die nächste Projektgruppe: 
Es muss eine Server-Funktionalität implementiert werden, die die Befehle `delete_expired_accounts` und `feedback` in regelmäßigen Abständen ausführt. Unter Linux kann dies beispielsweise über einen Cronjob realisiert werden.

## Wichtige Info Typescript-kompilieren
Aufgrund technischer Probleme wurde der Blur-Effekt bei Account-creation und Feedback-submission nur in Javascript geschrieben. Diese Funktionen müssten in Typescript übernommen werden, bevor die js-Datei durch das kompilieren der ts-Datei überschrieben wird.
