import logging
import logging.config
from typing import Any, Dict

from app.exceptions import LoggingConfigurationError


class LogSettings:
    """
    A class used to configure logging settings for the application.

    Methods
    -------
    __init__(log_level: str, log_format: str):
        Initializes the LogSettings instance with provided settings and configures logging.
    """

    def __init__(self, log_level: str, log_format: str) -> None:
        self.configure_logging(log_level, log_format)

    def configure_logging(self, log_level: str, log_format: str) -> None:
        """
        Configures logging settings.

        Args:
            log_level (str): The logging level.
            log_format (str): The logging format.

        Raises:
            LoggingConfigurationError: If there is an error configuring logging.
        """
        logging_config: Dict[str, Any] = self._get_logging_config(log_level, log_format)
        try:
            logging.config.dictConfig(logging_config)
            logging.info("Logging is configured.")
        except Exception as e:
            raise LoggingConfigurationError(f"Error configuring logging: {e}")

    @staticmethod
    def _get_logging_config(log_level: str, log_format: str) -> Dict[str, Any]:
        """
        Returns the logging configuration dictionary.

        Args:
            log_level (str): The logging level.
            log_format (str): The logging format.

        Returns:
            Dict[str, Any]: The logging configuration dictionary.
        """
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": log_format,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": log_level,
                },
            },
            "root": {
                "handlers": ["console"],
                "level": log_level,
            },
        }
