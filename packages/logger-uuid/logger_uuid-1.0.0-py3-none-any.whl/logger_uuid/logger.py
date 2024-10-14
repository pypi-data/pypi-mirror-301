import logging
from enum import Enum
from typing import Callable
from uuid import uuid4


class Logger:
    class LoggingLevelEnum(int, Enum):
        DEBUG = logging.DEBUG
        INFO = logging.INFO
        WARNING = logging.WARNING
        ERROR = logging.ERROR
        CRITICAL = logging.CRITICAL

    def __init__(self, process_id: str = None, level: str = "INFO"):
        self._process_id: str = process_id or str(uuid4())
        self._level: int = self._get_logging_level(level)

        logging.basicConfig(
            format="%(asctime)s [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=self._level,
            force=True,
        )
        self._logger: logging.Logger = logging.getLogger()

    @staticmethod
    def _get_logging_level(level: str) -> int:
        try:
            return Logger.LoggingLevelEnum[level.upper()]
        except KeyError:
            raise ValueError(f"Invalid logging level: {level}. "
                             f"Use one of: {', '.join(Logger.LoggingLevelEnum.__members__.keys())}")

    @property
    def process_id(self) -> str:
        return self._process_id

    @property
    def level(self) -> int:
        return self._level

    def _log(self, log_func: Callable, msg: str) -> None:
        log_func(f"{self._process_id}: {msg}")

    def log_debug(self, msg: str) -> None:
        self._log(self._logger.debug, msg)

    def log_info(self, msg: str) -> None:
        self._log(self._logger.info, msg)

    def log_warning(self, msg: str) -> None:
        self._log(self._logger.warning, msg)

    def log_error(self, msg: str) -> None:
        self._log(self._logger.error, msg)

    def log_critical(self, msg: str) -> None:
        self._log(self._logger.critical, msg)

    def log_exception(self, msg: str) -> None:
        self._log(self._logger.exception, msg)
