"""Responsible for any logging action."""
import logging


def log_config() -> None:
    """Config Logging Location."""
    logging.basicConfig(
        filename="task.log", encoding="utf-8", level=logging.DEBUG
    )
