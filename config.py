import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    TENANT_ID = os.getenv('TENANT_ID')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SOURCE_URL = os.getenv('SOURCE_URL')
    DESTINATION_SITE = os.getenv('DESTINATION_SITE')
    MAX_RETRIES = os.getenv('MAX_RETRIES', 3)  # Default to 3 retries if not specified