#!/usr/bin/env bash
set -euo pipefail

DB_URL=${DATABASE_URL:-"postgresql://convoca:convoca@localhost:5432/convocafinder"}

read -r -d '' SQL <<'SQL'
INSERT INTO sources (name, url, type, access_method, frequency_hours, is_active, robots_status, tos_notes)
VALUES
  ('Fondos Estatales CL', 'https://fondos.gob.cl/convocatorias', 'html_static', 'HTML', 12, true, 'allowed', 'Robots permite /convocatorias'),
  ('F6S Challenges', 'https://www.f6s.com/programs', 'html_dynamic', 'SPA', 6, true, 'allowed', 'Scraping permitido segun robots, revisar ToS'),
  ('Startup Chile API', 'https://api.startupchile.org/calls', 'api', 'API', 24, true, 'restricted', 'Solicitar API key oficial antes de producción')
ON CONFLICT (name) DO NOTHING;
SQL

psql "$DB_URL" -c "$SQL"
