@echo off
setlocal
cd /d "%~dp0"

COPY /Y .env.dev .env
if errorlevel 1 exit /b 1

call npm install
if errorlevel 1 exit /b 1

call npm run build
if errorlevel 1 exit /b 1

docker compose -f docker-compose.migrate.yml run --rm migrate upgrade head
if errorlevel 1 exit /b 1

docker compose -f docker-compose.seed.yml run --rm seed /app/app/fixtures/booksFactory.py
if errorlevel 1 exit /b 1

docker compose up
