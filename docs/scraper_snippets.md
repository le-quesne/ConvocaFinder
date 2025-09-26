# Ejemplos de entradas raw

## Fuente 1 - Portal estatal (HTML estático)
```html
<div class="call-card">
  <h3>Convocatoria Nacional de Innovación 2025</h3>
  <a href="https://fondos.gob.cl/convocatoria/123">Ver más</a>
  <span class="organizer">Ministerio de Ciencia</span>
  <span class="deadline">2025-10-15</span>
  <span class="country">Chile</span>
  <p class="description">Beca para proyectos...</p>
</div>
```

## Fuente 2 - SPA dinámica (Playwright)
```html
<div data-call>
  <div class="title">F6S Climate Challenge</div>
  <div class="organizer">F6S</div>
  <div class="deadline" data-date="01/12/2025"></div>
  <div class="country">Global</div>
  <div class="description">Programa intensivo...</div>
  <a href="https://www.f6s.com/climate-challenge">Postular</a>
</div>
```

## Fuente 3 - API/RSS
```json
{
  "calls": [
    {
      "id": "orig-12345",
      "title": "Convocatoria Nacional de Innovación 2025",
      "description": "Beca para proyectos...",
      "organizer": "Ministerio de Ciencia",
      "country": "Chile",
      "region": "Región Metropolitana",
      "published_at": "2025-09-01T00:00:00",
      "deadline": "2025-10-15T00:00:00",
      "amount": 500000,
      "currency": "CLP",
      "funding_type": "subvencion",
      "requirements": ["ser pyme", "tener RUT"],
      "url": "https://fondos.gob.cl/convocatoria/123",
      "tags": ["innovacion", "tecnologia"]
    }
  ]
}
```
