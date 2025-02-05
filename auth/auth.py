import msal
import logging
import os
from config import Config
from exceptions import TokenAcquisitionError


def get_access_token():
    """Acquire an access token using MSAL."""
    logging.info("Starting token acquisition process")
    config = Config()
    logging.info(f"Certificate path: {config.CERTIFICATE_PATH}")
    if not os.path.exists(config.CERTIFICATE_PATH):
        logging.error("Certificate file not found")
        raise TokenAcquisitionError("Certificate file not found")

    try:
        with open(config.CERTIFICATE_PATH, 'r') as cert_file:
            private_key = cert_file.read()
    except FileNotFoundError:
        logging.error("Certificate file not found")
        raise TokenAcquisitionError("Certificate file not found")

    app = msal.ConfidentialClientApplication(
        config.CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{config.TENANT_ID}",
        client_credential={
            "thumbprint": config.THUMBPRINT,
            "private_key": private_key,
        },
    )
    result = app.acquire_token_for_client(scopes=[config.API_SCOPE])
    if "access_token" in result:
        logging.info("Token acquisition successful")
        return result["access_token"]
    else:
        logging.error("Failed to obtain access token", result)
        raise TokenAcquisitionError("Failed to obtain access token")
