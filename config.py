import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    TENANT_ID = os.getenv('TENANT_ID')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SOURCE_URL = os.getenv('SOURCE_URL')
    FOLDER_PATH = os.getenv('FOLDER_PATH')
    API_SCOPE = os.getenv('API_SCOPE')
    DESTINATION_SITE = os.getenv('DESTINATION_SITE')
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))  # Convert to int
    CERTIFICATE_PATH = os.getenv('CERTIFICATE_PATH')
    CERTIFICATE_PASSWORD = os.getenv('CERTIFICATE_PASSWORD')
    THUMBPRINT = os.getenv('THUMBPRINT')