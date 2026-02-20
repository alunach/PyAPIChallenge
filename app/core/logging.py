from __future__ import annotations

import logging
import sys
from pythonjsonlogger import jsonlogger

def configure_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(level.upper())

    handler = logging.StreamHandler(sys.stdout)
    fmt = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s %(path)s"
    )
    handler.setFormatter(fmt)

    # Replace existing handlers
    root.handlers = [handler]
