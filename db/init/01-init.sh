#!/bin/bash
# Se ejecuta UNA sola vez, cuando el volumen de Postgres está vacío. Corre como POSTGRES_USER (superusuario).
# - Habilita pgvector en la BD de la aplicación (un rol sin privilegios no puede crear la extensión).
# - Crea el rol de la aplicación SIN superusuario y le da la BD y el esquema public.
# - Crea el rol y la BD de Keycloak (separados de los de la aplicación).
# Los nombres y contraseñas se pasan como variables de psql (:"nombre" / :'texto'), así que
# se citan correctamente aunque contengan comillas u otros caracteres especiales.
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$APP_DB_NAME" \
  -v app_db="$APP_DB_NAME" -v app_user="$APP_DB_USER" -v app_pw="$APP_DB_PASSWORD" \
  -v kc_db="$KC_DB_NAME" -v kc_user="$KC_DB_USER" -v kc_pw="$KC_DB_PASSWORD" <<-'EOSQL'
  CREATE EXTENSION IF NOT EXISTS vector;

  CREATE ROLE :"app_user" LOGIN PASSWORD :'app_pw' NOSUPERUSER NOCREATEDB NOCREATEROLE;
  ALTER DATABASE :"app_db" OWNER TO :"app_user";
  ALTER SCHEMA public OWNER TO :"app_user";

  CREATE ROLE :"kc_user" LOGIN PASSWORD :'kc_pw' NOSUPERUSER NOCREATEDB NOCREATEROLE;
  CREATE DATABASE :"kc_db" OWNER :"kc_user";
EOSQL

echo "Init listo: BD '$APP_DB_NAME' (dueño $APP_DB_USER, con pgvector) y BD '$KC_DB_NAME' (dueño $KC_DB_USER)."
