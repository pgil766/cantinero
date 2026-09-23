#!/bin/bash
# Se ejecuta UNA sola vez, cuando el volumen de Postgres está vacío.
# - Habilita pgvector en la BD de la aplicación.
# - Crea el usuario y la BD de Keycloak (separada de la de la aplicación).
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$APP_DB_NAME" <<-EOSQL
  CREATE EXTENSION IF NOT EXISTS vector;
  CREATE USER "$KC_DB_USER" WITH PASSWORD '$KC_DB_PASSWORD';
  CREATE DATABASE "$KC_DB_NAME" OWNER "$KC_DB_USER";
EOSQL

echo "BD '$APP_DB_NAME' con pgvector y BD '$KC_DB_NAME' para Keycloak creadas."
