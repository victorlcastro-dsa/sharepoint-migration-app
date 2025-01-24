import msal
import logging
from config import Config
from exceptions import TokenAcquisitionError

def get_access_token():
    """Acquire an access token using MSAL."""
    logging.info("Starting token acquisition process")
    config = Config()
    with open(config.CERTIFICATE_PATH, 'r') as cert_file:
        private_key = cert_file.read()

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