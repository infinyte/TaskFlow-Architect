# src/infrastructure/logging/logger.py
from abc import ABC, abstractmethod
from typing import Optional, Any
import logging

class Logger(ABC):
    @abstractmethod
    def info(self, message: str, meta: Optional[dict] = None) -> None:
        pass

    @abstractmethod
    def error(self, message: str, error: Optional[Exception] = None, meta: Optional[dict] = None) -> None:
        pass

    @abstractmethod
    def warn(self, message: str, meta: Optional[dict] = None) -> None:
        pass

    @abstractmethod
    def debug(self, message: str, meta: Optional[dict] = None) -> None:
        pass

class ConsoleLogger(Logger):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def info(self, message: str, meta: Optional[dict] = None) -> None:
        self.logger.info(message, extra=meta or {})

    def error(self, message: str, error: Optional[Exception] = None, meta: Optional[dict] = None) -> None:
        self.logger.error(message, exc_info=error, extra=meta or {})

    def warn(self, message: str, meta: Optional[dict] = None) -> None:
        self.logger.warning(message, extra=meta or {})

    def debug(self, message: str, meta: Optional[dict] = None) -> None:
        self.logger.debug(message, extra=meta or {})
