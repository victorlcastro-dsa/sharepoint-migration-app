import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TENANT_ID = os.getenv('TENANT_ID')
    TENANT_NAME = os.getenv('TENANT_NAME')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    API_SCOPE = os.getenv('API_SCOPE')
    ORIGIN_URL = os.getenv('ORIGIN_URL')
    DESTINATION_URL = os.getenv('DESTINATION_URL')
    CERTIFICATE_PATH = os.getenv('CERTIFICATE_PATH')
    THUMBPRINT = os.getenv('THUMBPRINT')