#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Gunakan pg_isready yang sudah terinstall (dari postgresql-client)
until PGPASSWORD=$DB_PASSWORD pg_isready -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL started"

# Start server langsung tanpa migration dan collectstatic
echo "Starting server..."
exec "$@"