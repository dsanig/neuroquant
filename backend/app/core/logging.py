import logging
import sys

import structlog

from app.core.config import settings


def setup_logging() -> None:
    logging.basicConfig(level=settings.log_level, format="%(message)s", stream=sys.stdout)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
