#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

cp -f .env.dev .env

npm install
npm run build

docker compose -f compose.migrate.yml run --rm migrate upgrade head
docker compose -f compose.seed.yml run --rm seed /app/app/fixtures/booksFactory.py
docker compose up
