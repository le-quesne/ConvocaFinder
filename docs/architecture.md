# Arquitectura ConvocaFinder

## Visión general
- **Frontend**: Next.js + Chakra UI. Consume API REST para listar convocatorias, gestionar alertas y panel admin.
- **Backend**: FastAPI + SQLAlchemy. Expone endpoints REST, maneja autenticación JWT, deduplicado y notificaciones.
- **Scrapers**: Tres conectores (HTML estático, Playwright SPA, API/RSS) ejecutados por un worker con APScheduler.
- **Base de datos**: PostgreSQL con esquema normalizado para convocatorias, fuentes, usuarios, alertas, logs y versionado.
- **Mensajería**: SMTP (Mailhog en dev) y Telegram bot opcional.
- **Infraestructura**: Docker Compose local. Terraform para AWS (VPC, RDS, ECS/EC2, S3 logs). Observabilidad con logs JSON y métrica Prometheus.

## Diagramas

### Diagrama de arquitectura (alto nivel)
```
[Fuentes] --> [Scrapers Worker] --> [FastAPI Backend] --> [PostgreSQL]
                                         |               ^
                                         v               |
                                   [Notificaciones]   [Redis Rate limit]
                                         |
                                    [Email/Telegram]

[Frontend Next.js] <--> [FastAPI Backend]
```

### ERD (simplificado)
```
Users 1---* Alerts
Users 1---* Favorites *---1 Calls ---* CallVersions
Sources 1---* Calls
Sources 1---* ScrapeLogs
```

## Decisiones clave
- FastAPI permite tipado y documentación automática.
- SQLAlchemy + PostgreSQL para relaciones complejas y JSONB.
- Deduplicado via fingerprint (hash) + fuzzy matching (rapidfuzz).
- Worker APScheduler sencillo para MVP; escalable a Celery en futuro.
- Playwright instalado en imagen Python para manejar SPA.
- Notificaciones abstractas via `NotificationService` para extender a SMS.
- Observabilidad mediante logs estructurados y endpoint `/metrics/prometheus` compatible con Prometheus.

## Trade-offs
- Se usa SQLite en tests por velocidad; en producción se usa PostgreSQL.
- Playwright incrementa peso de imagen, pero es necesario para SPA.
- Rate limiting simple en Redis (IP-based) sin soporte de claves por usuario; suficiente para MVP.
- No se implementa cola persistente; APScheduler corre en worker único.
