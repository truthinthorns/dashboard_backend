# Dashboard Backend

This is the backend service for the Dashboard project, built with **FastAPI**, **Beanie**, and **MongoDB**.

---

## Local Setup (Linux Recommended)

### 1. Pull the MongoDB Docker image

```bash
docker pull mongo:4.4.6
```

### 2. Start the MongoDB Container

```bash
docker run --name my-mongo -d \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=user \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:4.4.6
```

### 3. Install dependencies and start api

```bash
cd dashboard_backend
poetry install
poetry run start
```
#### You would access Swagger at localhost:5000 at this point.

---

## Authentication

Authentication is handled via **JWT tokens**. Protected routes require a valid `Authorization: Bearer <token>` header. Currently, only the token endpoint (used to login) and the weather endpoint does not require auth.

---

## Docker Cleanup

To stop and remove the Mongo container:

```bash
docker stop my-mongo && docker rm my-mongo
OPTIONAL: docker rmi mongo:4.4.6
```
