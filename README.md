# Dockerfile

- [Python 3.10-Slim](https://hub.docker.com/_/python)

- [Postgres 14](https://hub.docker.com/_/postgres)

# Pip requirements

- [flask](https://flask.palletsprojects.com/en/2.1.x/)

- [flask sql alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

- [psycopg](https://www.psycopg.org/docs/install.html)

- [Werkzeug](https://werkzeug.palletsprojects.com/en/2.1.x/installationWerkzeug)

- [pyjwt](https://pyjwt.readthedocs.io/en/stable/)

# Pre-Requisites

[Docker Desktop](https://docs.docker.com/desktop/)

# Docker Commands

Open a PowerShell session inside the root folder of this repository.

Run this command to start deploying the API container
```powershell
docker compose up --build api
```

Run this command to enter the postgresql db container
```powershell
docker exec -it db psql -U postgres
```

# Postman

Software [Installation](https://www.postman.com/downloads/)

JSON Test [collection](https://www.getpostman.com/collections/37c6351577b1f3e9d8d2)
