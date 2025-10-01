"""Util functions."""
import logging


def setup_logging() -> None:
    """Configure logging output."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging initialised.")
