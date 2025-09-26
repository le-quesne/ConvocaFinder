from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
import logging
import sys
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter

from .core.config import get_settings
from .api import auth, calls, alerts, sources, metrics, scrape_logs
from .core.rate_limiter import rate_limit

settings = get_settings()
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.INFO))
logger = structlog.get_logger()
scrape_success_counter = Counter("scrape_success_total", "Scrapes exitosos")
scrape_failed_counter = Counter("scrape_failed_total", "Scrapes fallidos")

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_rate_limit(request: Request, call_next):
    if request.url.path.startswith("/metrics/prometheus"):
        return await call_next(request)
    rate_limit(request)
    response = await call_next(request)
    return response


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):  # pragma: no cover - logging path
    logger.exception("Unhandled error", path=str(request.url), error=str(exc))
    return JSONResponse(status_code=500, content={"detail": "Error interno"})


@app.get("/metrics/prometheus")
async def prometheus_metrics():
    return JSONResponse(content=generate_latest().decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(calls.router)
api_router.include_router(alerts.router)
api_router.include_router(sources.router)
api_router.include_router(metrics.router)
api_router.include_router(scrape_logs.router)

app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
