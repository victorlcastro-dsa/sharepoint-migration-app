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
        self.IGNORE_VERSION_HISTORY = os.getenv('IGNORE_VERSION_HISTORY', 'False').lower() == 'true'
        self.ALLOW_SCHEMA_MISMATCH = os.getenv('ALLOW_SCHEMA_MISMATCH', 'True').lower() == 'true'
        self.ALLOW_SMALLER_VERSION_LIMIT_ON_DESTINATION = os.getenv('ALLOW_SMALLER_VERSION_LIMIT_ON_DESTINATION', 'True').lower() == 'true'
        self.INCLUDE_ITEM_PERMISSIONS = os.getenv('INCLUDE_ITEM_PERMISSIONS', 'False').lower() == 'true'
        self.BYPASS_SHARED_LOCK = os.getenv('BYPASS_SHARED_LOCK', 'True').lower() == 'true'
        self.MOVE_BUT_KEEP_SOURCE = os.getenv('MOVE_BUT_KEEP_SOURCE', 'False').lower() == 'true'
        self.EXCLUDE_CHILDREN = os.getenv('EXCLUDE_CHILDREN', 'False').lower() == 'true'
        self.IS_MOVE_MODE = os.getenv('IS_MOVE_MODE', 'False').lower() == 'true'