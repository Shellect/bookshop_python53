#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

cp -f .env.dev .env
npm install
npm run build

docker compose -f docker-compose.migrate.yml run --rm migrate upgrade head
docker compose -f docker-compose.seed.yml run --rm seed /app/app/fixtures/booksFactory.py
docker compose up
