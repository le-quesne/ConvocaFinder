# Guía de seguridad y cumplimiento ConvocaFinder

## Checklist al integrar nuevas fuentes
1. **Revisar robots.txt**: documentar ruta y estatus (`allowed`, `disallowed`, `rate-limited`).
2. **Analizar Términos de Servicio**: identificar cláusulas sobre scraping, caching, redistribución y atribución. Registrar resumen en `sources.tos_notes`.
3. **Preferir API oficial**: si existe endpoint oficial, contactar al operador para obtener clave/API key. Evitar scraping si los Términos lo prohíben expresamente.
4. **Respeto a límites**: configurar frecuencia acorde al `crawl-delay` o recomendaciones oficiales. Ajustar `frequency_hours`.
5. **Datos personales**: evitar almacenar información sensible; incluir origen explícito si se almacenan correos públicos.
6. **Logs de acceso**: habilitar logging para detectar bloqueos o cambios en HTML.

## Auditorías periódicas
- **Trimestral**: revisar cada fuente para confirmar que los Términos no cambiaron. Actualizar `tos_notes` y contacto.
- **Alertas automáticas**: configurar notificación en Sentry/Slack si un scraper falla >3 veces consecutivas.
- **Reportes**: generar reporte de scraping (`scrape_logs`) exportable para revisión legal.

## Seguridad de la plataforma
- Contraseñas hasheadas con bcrypt, tokens JWT con expiración 24h.
- Rate limiting por IP (Redis). En producción se recomienda API Gateway/WAF.
- Variables de entorno gestionadas via Secret Manager (AWS Secrets Manager sugerido).
- Backups automáticos RDS (7 días) y versionado S3.
- Monitoreo `/metrics/prometheus` + integración Sentry para excepciones críticas.

## Respuesta ante incidentes
1. Desactivar fuente (`sources.is_active=false`) ante sospecha de incumplimiento.
2. Notificar a usuarios si una convocatoria se elimina o corrige.
3. Revisar logs para identificar qué datos se recopilaron y tomar medidas correctivas.
