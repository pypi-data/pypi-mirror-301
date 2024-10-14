"""Top-level package for Athlon Flex API."""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_format = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

from athlon_flex_api.api import AthlonFlexApi  # noqa: E402

__all__ = ["logger", "api", "vehicles_clusters", "AthlonFlexApi"]
