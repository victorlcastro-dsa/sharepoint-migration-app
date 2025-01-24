import msal
from config import Config

# Function to get the access token
def get_access_token(tenant_id, client_id, certificate_path):
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
        return result["access_token"]
    else:
        raise Exception("Failed to obtain access token", result)