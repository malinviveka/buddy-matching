# buddy-matching
Repository für das Matching-Software-Projekt

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