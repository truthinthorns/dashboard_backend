To get this started locally, ideally on Linux, do the following:
    - docker pull mongo:4.4.6
    - docker run --name my-mongo -d -p 27017:27017   -e MONGO_INITDB_ROOT_USERNAME=user   -e MONGO_INITDB_ROOT_PASSWORD=password   mongo:4.4.6
    - inside /dashboard_backend
        - poetry install
        - poetry run start
