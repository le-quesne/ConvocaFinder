# ConvocaFinder

Sistema SaaS para agregar, normalizar y notificar convocatorias y fondos para emprendedores.

## Contenido
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Quickstart (Docker)](#quickstart-docker)
- [Scrapers y fuentes](#scrapers-y-fuentes)
- [Notificaciones](#notificaciones)
- [Pruebas](#pruebas)
- [Deploy con Terraform](#deploy-con-terraform)
- [Cumplimiento legal y ética](#cumplimiento-legal-y-ética)
- [API](#api)
- [Observabilidad](#observabilidad)
- [Datos de ejemplo](#datos-de-ejemplo)

## Características
- API REST FastAPI con autenticación JWT, filtros avanzados y panel admin de fuentes.
- Scrapers modulares (HTML estático, SPA Playwright, API/RSS) con deduplicado por fingerprint y fuzzy matching.
- Notificaciones por email y Telegram según alertas definidas por usuarios.
- Dashboard Next.js con filtros, favoritos, alertas y panel admin.
- Infraestructura como código (Terraform AWS + Docker Compose) y pipeline CI GitHub Actions.

## Arquitectura
Consulta `docs/architecture.md` para diagramas y decisiones clave.

## Requisitos
- Docker y docker-compose (o `docker compose`).
- Make (opcional) y bash.
- Para Playwright en local es necesario ejecutar `npx playwright install` si se corre fuera de Docker.

## Quickstart (Docker)

```bash
cp .env.example .env
docker compose build --no-cache
docker compose up -d
Backend: http://localhost:8000/docs
Frontend: http://localhost:3000
Mailhog: http://localhost:8025
Inicializar base de datos
# Crear DB (si no existe)
docker compose exec -e PGPASSWORD=convoca db \
  psql -U convoca -d postgres -c "CREATE DATABASE convocafinder OWNER convoca;"

# Cargar schema.sql
docker compose exec backend bash -lc 'cat /app/schema.sql' \
  | docker compose exec -T db bash -lc 'PGPASSWORD=convoca psql -U convoca -d convocafinder'

# Ver tablas
docker compose exec -T db bash -lc \
  'PGPASSWORD=convoca psql -U convoca -d convocafinder -c "\dt"'
Poblar datos / probar scrapers
docker compose exec backend python -c \
"from app.services.scraper_runner import run_all_scrapers; print(run_all_scrapers())"
Troubleshooting común
Playwright falla en build: usamos base mcr.microsoft.com/playwright/python:v1.41.1-jammy.
Frontend no abre: ejecutar con -H 0.0.0.0 -p 3000 y exponer 3000:3000.
next: not found: asegurarse de npm ci en build y volumen frontend_node_modules.
CORS / Pydantic JSON: CORS_ORIGINS=["http://localhost:3000"] (JSON).
DB "convoca" no existe: URL correcta .../convocafinder y crear DB si falta.
```

## Scrapers y fuentes
| Fuente | Tipo | Método | Frecuencia sugerida | Estado legal |
|--------|------|--------|---------------------|--------------|
| Fondos Estatales CL | html_static | Scraping HTML (requests+BS4) | 12h | Permitido (robots.txt permite /convocatorias) |
| F6S Challenges | html_dynamic | Playwright SPA | 6h | Permitido (robots.txt permite, revisar ToS para uso comercial) |
| Startup Chile API | api | API JSON | 24h | Requiere solicitar API key oficial antes de producción |

Cada scraper registra métricas y logs en la tabla `scrape_logs`. Antes de activar una fuente nueva, ejecutar `robots.txt` check y documentar ToS en `sources.tos_notes`.

## Notificaciones
- Email vía SMTP configurable (Mailhog en local).
- Telegram opcional (definir `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHANNEL_ID`).
- Los nuevos registros activan notificaciones hacia usuarios con alertas activas (canal email) y Telegram broadcast.

## Pruebas
```bash
cd backend
pytest --cov=app
```
Incluye tests unitarios de deduplicado y scrapers con mocks y un test de integración API.

## Deploy con Terraform
1. Configura credenciales AWS (`aws configure`).
2. Ve a `infra/terraform` y crea `terraform.tfvars`:
   ```hcl
   db_username = "convoca"
   db_password = "cambia-esto"
   environment = "staging"
   ```
3. Ejecuta:
   ```bash
   cd infra/terraform
   terraform init
   terraform apply
   ```
Esto crea VPC, RDS PostgreSQL y bucket S3 para logs. Para desplegar la app usar ECS/EKS (tareas comentadas como referencia) o EC2 con Docker Compose.

## Cumplimiento legal y ética
- Verificar `robots.txt` y Términos de Servicio antes de scrapear. Si se prohíbe el scraping (ej. ciertos portales privados), detener y solicitar acceso oficial.
- No almacenar datos personales sensibles; si una convocatoria publica emails o teléfonos, mantener referencia a la fuente.
- Mantener logs de verificación `robots_status` y notas en `sources.tos_notes`.
- Auditoría periódica: revisar nuevas fuentes, asegurar que las credenciales API se obtengan mediante acuerdos.
- Política de uso responsable: agregar disclaimer en UI y al enviar emails.

## API
- Especificación OpenAPI en `docs/openapi.yaml`.
- Ejemplo `GET /convocatorias`:
```bash
curl "http://localhost:8000/convocatorias?country=Chile"
```
Respuesta ejemplo:
```json
{
  "data": [
    {
      "id": 1,
      "origin_id": "orig-12345",
      "title": "Convocatoria Nacional de Innovación 2025",
      "description": "Beca para proyectos...",
      "organizer": "Ministerio de Ciencia",
      "country": "Chile",
      "region": "Región Metropolitana",
      "published_at": "2025-09-01",
      "deadline": "2025-10-15",
      "amount": 500000,
      "currency": "CLP",
      "funding_type": "subvencion",
      "requirements": ["ser pyme", "tener RUT"],
      "source_url": "https://fondos.gob.cl/convocatoria/123",
      "tags": ["innovacion", "tecnologia"],
      "last_scraped_at": "2025-09-26T10:00:00"
    }
  ],
  "pagination": {
    "total": 1,
    "page": 1,
    "size": 20
  }
}
```

## Observabilidad
- Logs estructurados (stdout) con `structlog`.
- Endpoint `/metrics/prometheus` expone métricas básicas (scrapes success/fail) compatibles con Prometheus.
- Integración opcional con Sentry (`SENTRY_DSN`).

## Datos de ejemplo
- `seed_sources.sh` inserta las 3 fuentes.
- `docs/scraper_snippets.md` incluye ejemplos raw.
- `docs/PLAN.md` detalla plan de trabajo.

## Seguridad
- Hash de contraseñas con bcrypt.
- Rate limiting por IP (Redis).
- Variables de entorno para credenciales.
- Revisar `docs/architecture.md` para recomendaciones adicionales.
