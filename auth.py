import msal
import logging
from config import Config

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get the access token
def get_access_token(tenant_id, client_id, certificate_path):
    logging.info("Starting token acquisition process")
    with open(certificate_path, 'r') as cert_file:
        private_key = cert_file.read()

    app = msal.ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential={
            "thumbprint": Config.THUMBPRINT,
            "private_key": private_key,
            # Remove "passphrase" if the private key is not encrypted
        },
    )
    result = app.acquire_token_for_client(scopes=[Config.API_SCOPE])
    if "access_token" in result:
        logging.info("Token acquisition successful")
        return result["access_token"]
    else:
        logging.error("Failed to obtain access token", result)
        raise Exception("Failed to obtain access token", result)