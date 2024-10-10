from datetime import datetime as _datetime
import logging as _logging
import sys as _sys

from .client import GasEstimate, MachClient, Order, Quote, WalletPoints, client
from .constants import ChainId, Scanner
from .data_types import Chain, Token
from .log import LogContextAdapter, Logger

__all__ = [
    "Chain",
    "ChainId",
    "GasEstimate",
    "LogContextAdapter",
    "Logger",
    "MachClient",
    "Order",
    "Quote",
    "Scanner",
    "Token",
    "WalletPoints",
    "client",
]


def _make_logger(name: str) -> _logging.Logger:
    logger = _logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(_logging.DEBUG)

    handler = _logging.StreamHandler(_sys.stdout)
    handler.setLevel(_logging.DEBUG)
    logger.addHandler(handler)

    logger.info(f"START {name} {_datetime.today()}")

    return logger


_make_logger("mach-client")
