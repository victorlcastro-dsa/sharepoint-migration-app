import os
from typing import Optional

from dotenv import load_dotenv

from app.exceptions import EnvironmentVariableError


class Settings:
    """
    A class used to load and store configuration settings from environment variables.

    Attributes
    ----------
    LOG_LEVEL : str
        The logging level.
    LOG_FORMAT : str
        The logging format.
    CLIENT_ID : str
        The client ID for authentication.
    TENANT_ID : str
        The tenant ID for authentication.
    TENANT_NAME : str
        The tenant name for authentication.
    THUMBPRINT : str
        The thumbprint of the certificate.
    CERTIFICATE_PATH : str
        The path to the certificate file.
    API_SCOPE : str
        The API scope for authentication.
    ORIGIN_URL : str
        The origin URL of the SharePoint site.
    PARTIAL_ORIGIN_URL : str
        The partial URL of the SharePoint site.
    FETCH_FILENAME : str
        The filename for the fetched SharePoint folder structure.
    BASE_URL : str
        The base URL of the SharePoint site.
    IS_MOVE_MODE : bool
        Whether to move items instead of copying.
    IGNORE_VERSION_HISTORY : bool
        Whether to ignore version history.
    ALLOW_SCHEMA_MISMATCH : bool
        Whether to allow schema mismatch.
    ALLOW_SMALLER_VERSION_LIMIT_ON_DESTINATION : bool
        Whether to allow smaller version limit on destination.
    INCLUDE_ITEM_PERMISSIONS : bool
        Whether to include item permissions.
    BYPASS_SHARED_LOCK : bool
        Whether to bypass shared lock.
    MOVE_BUT_KEEP_SOURCE : bool
        Whether to move but keep source.
    EXCLUDE_CHILDREN : bool
        Whether to exclude children.
    LEVEL : int
        The level of items to create copy jobs for.
    DESTINATION_URL : str
        The destination URL for the copy jobs.
    AIOHTTP_LIMIT : int
        The connection limit for aiohttp.

    Methods
    -------
    __init__():
        Initializes the Settings instance and loads environment variables.
    """

    def __init__(self) -> None:
        """
        Initializes the Settings instance and loads environment variables.
        """
        load_dotenv()
        self.LOG_LEVEL: str = self._get_env_var("LOG_LEVEL", "INFO").upper()
        self.LOG_FORMAT: str = self._get_env_var(
            "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.CLIENT_ID: str = self._get_env_var("CLIENT_ID")
        self.TENANT_ID: str = self._get_env_var("TENANT_ID")
        self.TENANT_NAME: str = self._get_env_var("TENANT_NAME")
        self.THUMBPRINT: str = self._get_env_var("THUMBPRINT")
        self.CERTIFICATE_PATH: str = self._get_env_var("CERTIFICATE_PATH")
        self.API_SCOPE: str = self._get_env_var("API_SCOPE")
        self.ORIGIN_URL: str = self._get_env_var("ORIGIN_URL")
        self.PARTIAL_ORIGIN_URL: str = self._get_env_var("PARTIAL_ORIGIN_URL")
        self.FETCH_FILENAME: str = self._get_env_var("FETCH_FILENAME")
        self.BASE_URL: str = self._get_env_var("BASE_URL")
        self.IS_MOVE_MODE: bool = (
            self._get_env_var("IS_MOVE_MODE", "False").lower() == "true"
        )
        self.IGNORE_VERSION_HISTORY: bool = (
            self._get_env_var("IGNORE_VERSION_HISTORY", "False").lower() == "true"
        )
        self.ALLOW_SCHEMA_MISMATCH: bool = (
            self._get_env_var("ALLOW_SCHEMA_MISMATCH", "False").lower() == "true"
        )
        self.ALLOW_SMALLER_VERSION_LIMIT_ON_DESTINATION: bool = (
            self._get_env_var(
                "ALLOW_SMALLER_VERSION_LIMIT_ON_DESTINATION", "False"
            ).lower()
            == "true"
        )
        self.INCLUDE_ITEM_PERMISSIONS: bool = (
            self._get_env_var("INCLUDE_ITEM_PERMISSIONS", "False").lower() == "true"
        )
        self.BYPASS_SHARED_LOCK: bool = (
            self._get_env_var("BYPASS_SHARED_LOCK", "False").lower() == "true"
        )
        self.MOVE_BUT_KEEP_SOURCE: bool = (
            self._get_env_var("MOVE_BUT_KEEP_SOURCE", "False").lower() == "true"
        )
        self.EXCLUDE_CHILDREN: bool = (
            self._get_env_var("EXCLUDE_CHILDREN", "False").lower() == "true"
        )
        self.LEVEL: int = int(self._get_env_var("LEVEL", 0))
        self.DESTINATION_URL: str = self._get_env_var("DESTINATION_URL")
        self.AIOHTTP_LIMIT: int = int(self._get_env_var("AIOHTTP_LIMIT", 10))

    @staticmethod
    def _get_env_var(name: str, default: Optional[str] = None) -> str:
        """
        Gets an environment variable or returns a default value.

        Args:
            name (str): The name of the environment variable.
            default (Optional[str]): The default value if the environment variable is not set.

        Returns:
            str: The value of the environment variable or the default value.

        Raises:
            EnvironmentVariableError: If the environment variable is not set and no default value is provided.
        """
        value = os.getenv(name, default)
        if value is None:
            raise EnvironmentVariableError(
                f"Environment variable {name} is not set and no default value provided."
            )
        return value
