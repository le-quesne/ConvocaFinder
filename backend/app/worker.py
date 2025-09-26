import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from .services.scraper_runner import run_all_scrapers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def job():
    logger.info("Ejecutando scrapers")
    results = run_all_scrapers()
    logger.info("Resultados scrapers: %s", results)


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_all_scrapers, "interval", hours=6, id="scraper_job")
    scheduler.start()
    logger.info("Worker iniciado")
    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    main()
