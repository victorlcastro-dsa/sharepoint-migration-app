import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.TENANT_ID = os.getenv('TENANT_ID')
        self.TENANT_NAME = os.getenv('TENANT_NAME')
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        self.API_SCOPE = os.getenv('API_SCOPE')
        self.ORIGIN_URL = os.getenv('ORIGIN_URL')
        self.DESTINATION_URL = os.getenv('DESTINATION_URL')
        self.CERTIFICATE_PATH = os.getenv('CERTIFICATE_PATH')
        self.THUMBPRINT = os.getenv('THUMBPRINT')
        self.LOG_FILE = os.getenv('LOG_FILE', 'app.log')
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.INITIAL_DELAY = int(os.getenv('INITIAL_DELAY', 10))
        self.INTERVAL = int(os.getenv('INTERVAL', 60))
        self.MAX_INITIAL_WAIT = int(os.getenv('MAX_INITIAL_WAIT', 120))