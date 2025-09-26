# Plan de Trabajo ConvocaFinder

## Milestones y estimación

1. **Arquitectura y preparación de entorno** (6h)
   - Definir stack tecnológico (FastAPI, PostgreSQL, Next.js, Terraform).
   - Configurar estructura de repo, Docker, dependencias base.
   - Entregables: repositorio inicial, docker-compose base.

2. **Diseño de base de datos y modelos** (8h)
   - Crear esquema relacional normalizado, migraciones iniciales.
   - Implementar ORM y modelos Pydantic.
   - Entregables: `schema.sql`, modelos SQLAlchemy, seeds iniciales.

3. **Implementación API backend** (18h)
   - Endpoints de autenticación, convocatorias, alertas y fuentes.
   - Lógica de filtros, paginación, deduplicado y versionado simple.
   - Integración de notificaciones y observabilidad (metrics/logs).

4. **Scrapers e ingesta** (16h)
   - Conectores para 3 fuentes (estática, dinámica, API/RSS).
   - Scheduler y worker para ejecutar scrapers, registrar métricas.
   - Tests unitarios de parsers y deduplicado (>60% cobertura).

5. **Frontend Dashboard** (14h)
   - Autenticación, listado de convocatorias, filtros, alertas.
   - Panel admin básico para fuentes y estado de scraping.
   - Disclaimer legal visible.

6. **Notificaciones y mensajería** (6h)
   - Integración SMTP (enviar via Mailhog en dev) y Telegram bot.
   - Simulaciones en entorno local y hooks en worker.

7. **Infraestructura y CI/CD** (10h)
   - Terraform para AWS (VPC, RDS, ECS Fargate/EC2, S3 logs).
   - Workflow GitHub Actions (lint, tests, build containers).
   - Scripts de despliegue (`seed_sources.sh`, documentación).

8. **Documentación y compliance** (6h)
   - README completo, guía legal/ética, OpenAPI, diagramas.
   - Instrucciones de staging y seguridad.

**Total estimado**: ~84 horas distribuidas en 2-3 semanas.

## Riesgos y mitigaciones
- **Cambios en HTML**: diseñar scrapers modulares con selectores versionados y alertas de error.
- **Limitaciones legales**: verificación `robots.txt` antes de scrapear, mantener registro en DB, solicitar APIs cuando se requiera.
- **Escalabilidad**: uso de colas y contenedores escalables en futuro; para MVP se deja preparado.
