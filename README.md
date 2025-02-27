# SharePoint Migration App

## Overview

The SharePoint Migration App is a Python-based application designed to facilitate the migration of folder structures and files from one SharePoint site to another. The application fetches the folder structure from the source SharePoint site, saves it to an Excel file, and creates copy jobs to transfer the files to the destination SharePoint site.

## Features

- **Authentication**: Uses Microsoft Authentication Library (MSAL) to acquire access tokens for SharePoint API.
- **Logging**: Configurable logging settings to monitor the application's activities.
- **Configuration**: Loads configuration settings from environment variables.
- **Fetch Structure**: Fetches the folder structure from the source SharePoint site using REST API.
- **Export to Excel**: Saves the fetched folder structure to an Excel file.
- **Create Copy Jobs**: Creates copy jobs in SharePoint to transfer files from the source to the destination site.

## TODOs
```
# TODO: Implement monitoring of copy jobs
# TODO: Implement filtering of items by name or other criteria
# TODO: Add support for files, not just folders
# TODO: Allow customization of the migration process via the configuration file and command-line arguments
# TODO: Implement size validation to prevent exceeding SharePoint limits
# TODO: Implement count validation to prevent exceeding SharePoint limits
# TODO: Ensure the copy operation preserves the full folder hierarchy, even when copying a specific file or subfolder.
```

## Project Structure
```
.
├── .env
├── .gitignore
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── authenticator.py
│   │   └── certificate_loader.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── log_settings.py
│   │   └── settings.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── sharepoint_folder_structure.xlsx
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── asyncio_exceptions.py
│   │   ├── authentication_exceptions.py
│   │   ├── certificate_exceptions.py
│   │   ├── configuration_exceptions.py
│   │   ├── excel_exceptions.py
│   │   ├── job_exceptions.py
│   │   ├── main_exceptions.py
│   │   └── sharepoint_exceptions.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── create_copy_jobs.py
│   │   ├── create_excel.py
│   │   ├── fetch_structure.py
│   │   └── monitor_jobs.py
│   └── utils/
│       └── __init__.py
├── certificate.pem
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd sharepoint-migration-app
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory with the following content:
    ```ini
    # Tenant Identification
    TENANT_ID="your-tenant-id"  # Azure AD tenant ID
    TENANT_NAME="your-tenant-name"  # Azure AD tenant name

    # Client Credentials
    CLIENT_ID="your-client-id"  # Client ID of the registered application in Azure AD
    CLIENT_SECRET="your-client-secret"  # Client secret of the registered application in Azure AD

    # Source and Destination URLs
    ORIGIN_URL="your-origin-url"  # Source SharePoint site URL
    PARTIAL_ORIGIN_URL="your-partial-origin-url"  # Partial URL of the source SharePoint site
    DESTINATION_URL="your-destination-url"  # Destination SharePoint site URL
    BASE_URL="your-base-url"  # Base URL of the SharePoint site

    # API Configurations
    API_SCOPE="your-api-scope"  # API scope for authentication
    CERTIFICATE_PATH="./certificado_completo.pem"  # Path to the certificate file
    THUMBPRINT="your-thumbprint"  # Thumbprint of the certificate

    # Log Configurations
    LOG_LEVEL="DEBUG"  # Log level
    LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Log format

    # Migration Configurations
    IGNORE_VERSION_HISTORY=False  # Ignore version history
    ALLOW_SCHEMA_MISMATCH=True  # Allow schema mismatch
    ALLOW_SMALLER_VERSION_LIMIT_ON_DESTINATION=True  # Allow smaller version limit on destination
    INCLUDE_ITEM_PERMISSIONS=False  # Include item permissions
    BYPASS_SHARED_LOCK=True  # Bypass shared lock
    MOVE_BUT_KEEP_SOURCE=False  # Move but keep source
    EXCLUDE_CHILDREN=False  # Exclude children
    IS_MOVE_MODE=False  # Move mode
    LEVEL=0  # Level of items to create copy jobs

    # Data File Configurations
    FETCH_FILENAME="sharepoint_folder_structure.xlsx"  # Filename for the SharePoint folder structure

    # aiohttp Configurations
    AIOHTTP_LIMIT=10  # Connection limit for aiohttp
    ```

## Usage

Run the main script:
```sh
python main.py
```

The application will:
1. Load configuration settings.
2. Configure logging.
3. Acquire an access token.
4. Fetch the SharePoint folder structure.
5. Save the structure to an Excel file.
6. Create copy jobs to transfer files to the destination site.

## Modules

- **Authenticator**: Located in `app/auth/authenticator.py`, this module handles the acquisition and management of access tokens using MSAL.
- **CertificateLoader**: Located in `app/auth/certificate_loader.py`, this module handles loading of certificates from a file.
- **LogSettings**: Located in `app/config/log_settings.py`, this module configures logging settings for the application.
- **Settings**: Located in `app/config/settings.py`, this module loads and stores configuration settings from environment variables.
- **SharePointStructureFetcher**: Located in `app/services/fetch_structure.py`, this module fetches the folder structure from the SharePoint site using REST API.
- **ExcelExporter**: Located in `app/services/create_excel.py`, this module handles exporting the SharePoint folder structure to an Excel file.
- **CopyJobsCreator**: Located in `app/services/create_copy_jobs.py`, this module creates copy jobs in SharePoint for items with the specified level.
- **MonitorJobs**: Located in `app/services/monitor_jobs.py`, this module is intended to monitor the status of copy jobs (currently empty).
