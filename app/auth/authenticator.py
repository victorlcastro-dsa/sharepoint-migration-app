import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import msal

from app.auth.certificate_loader import CertificateLoader
from app.exceptions import (
    AsyncioError,
    MSALAuthenticationError,
    TokenAcquisitionError,
)


class Authenticator:
    """
    The Authenticator class handles the acquisition and management of access tokens
    using the Microsoft Authentication Library (MSAL).

    Attributes:
        client_id (str): The client ID for authentication.
        tenant_id (str): The tenant ID for authentication.
        thumbprint (str): The thumbprint of the certificate.
        certificate_path (str): The path to the certificate file.
        api_scope (str): The API scope for authentication.
        access_token (Optional[str]): The current access token.
        token_expiry (Optional[datetime]): The expiry time of the current access token.

    Methods:
        __init__():
            Initializes the Authenticator instance with settings, access_token, and token_expiry.

        async get_access_token() -> str:
            Acquires an access token using MSAL. Reuses the existing token if it is still valid.

        _is_token_valid() -> bool:
            Checks if the current access token is valid based on its expiry time.

        _process_token_result(result: Dict[str, Any]) -> str:
            Processes the result of the token acquisition and updates the access token and expiry time.
    """

    def __init__(
        self,
        client_id: str,
        tenant_id: str,
        thumbprint: str,
        certificate_path: str,
        api_scope: str,
    ) -> None:
        """
        Initializes the Authenticator instance with settings, access_token, and token_expiry.
        """
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.thumbprint = thumbprint
        self.certificate_path = certificate_path
        self.api_scope = api_scope
        self.access_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None

    async def get_access_token(self) -> str:
        """
        Acquires an access token using MSAL. Reuses the existing token if it is still valid.

        Returns:
            str: The access token.

        Raises:
            TokenAcquisitionError: If the token acquisition fails.
            MSALAuthenticationError: If there is an error with MSAL authentication.
            AsyncioError: If there is an error with asyncio.
        """
        if self._is_token_valid():
            logging.info("Reusing existing access token")
            return self.access_token

        logging.info("Starting token acquisition process")
        private_key = CertificateLoader.load_certificate(self.certificate_path)

        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential={
                "thumbprint": self.thumbprint,
                "private_key": private_key,
            },
        )
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, app.acquire_token_for_client, [self.api_scope]
            )
        except msal.MsalServiceError as e:
            logging.error(f"MSAL service error: {e}")
            raise MSALAuthenticationError(f"MSAL service error: {e}")
        except msal.MsalClientError as e:
            logging.error(f"MSAL client error: {e}")
            raise MSALAuthenticationError(f"MSAL client error: {e}")
        except Exception as e:
            logging.error(f"Asyncio error: {e}")
            raise AsyncioError(f"Asyncio error: {e}")

        return self._process_token_result(result)

    def _is_token_valid(self) -> bool:
        """
        Checks if the current access token is valid based on its expiry time.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        return (
            self.access_token is not None
            and self.token_expiry is not None
            and datetime.now(timezone.utc) < self.token_expiry
        )

    def _process_token_result(self, result: Dict[str, Any]) -> str:
        """
        Processes the result of the token acquisition and updates the access token and expiry time.

        Args:
            result (Dict[str, Any]): The result of the token acquisition.

        Returns:
            str: The access token.

        Raises:
            TokenAcquisitionError: If the token acquisition fails.
        """
        if "access_token" in result:
            logging.info("Token acquisition successful")
            self.access_token = result["access_token"]
            self.token_expiry = datetime.now(timezone.utc) + timedelta(
                seconds=result["expires_in"]
            )
            return self.access_token
        else:
            logging.error("Failed to obtain access token", result)
            raise TokenAcquisitionError("Failed to obtain access token")
