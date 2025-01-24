# SharePoint Job Manager

This project is a SharePoint Job Manager that automates the process of creating and monitoring copy jobs in SharePoint. It uses the Microsoft Authentication Library (MSAL) to acquire access tokens and interact with the SharePoint API.

## Project Structure

## Project Structure

The project structure is as follows:

```
sharepoint-migration-app/
├── auth/
│   └── __init__.py
│   └── auth.py # Contains the authentication logic to acquire access tokens.
├── config/
│   └── __init__.py
│   └── config.py # Contains the configuration logic to load environment variables.
├── exceptions/
│   └── __init__.py
│   └── exceptions.py # Contains custom exception classes.
├── jobs/
│   └── __init__.py
│   └── jobs.py # Contains the main logic for creating and monitoring SharePoint copy jobs.
├── log_config/
│   └── __init__.py
│   └── logging_config.py # Contains the logging configuration.
├── utils/
│   └── __init__.py
│   └── utils.py # Contains utility functions for creating request headers and payloads.
├── run.py # The main entry point of the application.
├── requirements.txt # Lists the dependencies required for the project.
├── .env # Contains environment variables for configuration.
└── certificado_completo.pem # Contains the certificate and private key for authentication.
```

## Requirements

To run this project, you need the following:

- Python 3.6 or higher
- The dependencies listed in `requirements.txt`
- A valid SharePoint tenant and client credentials
- A certificate and private key for authentication
- An Azure app configured with the appropriate permissions
  - The app must have the necessary API permissions to access SharePoint
  - The account used must have admin or full access rights

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv sharepoint-env
    source sharepoint-env/bin/activate  # On Windows, use `sharepoint-env\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root directory with the following content:**

    ```properties
    TENANT_ID="your-tenant-id"
    CLIENT_ID="your-client-id"
    CLIENT_SECRET="your-client-secret"
    ORIGIN_URL="your-origin-url"
    DESTINATION_URL="your-destination-url"
    API_SCOPE="https://your-tenant-name.sharepoint.com/.default"
    CERTIFICATE_PATH="./certificado_completo.pem"
    THUMBPRINT="your-certificate-thumbprint"
    TENANT_NAME="your-tenant-name"
    LOG_FILE="app.log"
    LOG_LEVEL="INFO"
    INITIAL_DELAY=10
    INTERVAL=60
    MAX_INITIAL_WAIT=120
    IGNORE_VERSION_HISTORY=False
    ALLOW_SCHEMA_MISMATCH=True
    ALLOW_SMALLER_VERSION_LIMIT_ON_DESTINATION=True
    INCLUDE_ITEM_PERMISSIONS=False
    BYPASS_SHARED_LOCK=True
    MOVE_BUT_KEEP_SOURCE=False
    EXCLUDE_CHILDREN=False
    IS_MOVE_MODE=False
    ```

5. **Place your certificate and private key in a file named `certificado_completo.pem` in the root directory.**

## Running the Application

To run the application, execute the following command:

```sh
python run.py
```

The application will create a copy job in SharePoint.

```sh
#FIXME: Please note that the progress monitor currently cannot accurately determine if a job has completed.
```
