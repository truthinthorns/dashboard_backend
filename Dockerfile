FROM python:3.14-slim-bookworm
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml .
RUN poetry install --without dev --no-root
COPY . .
EXPOSE 5000
CMD ["poetry", "run", "start"]