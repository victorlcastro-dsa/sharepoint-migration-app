import asyncio
import logging
import os

from app.auth.authenticator import Authenticator
from app.config.log_settings import LogSettings
from app.config.settings import Settings
from app.exceptions import MainExecutionError
from app.services.create_copy_jobs import CopyJobsCreator
from app.services.create_excel import ExcelExporter
from app.services.fetch_structure import SharePointStructureFetcher


async def main() -> None:
    """
    The main function that configures logging, acquires an access token, fetches the SharePoint folder structure,
    saves it to an Excel file, and creates copy jobs based on a specified level.

    Raises:
        MainExecutionError: If an error occurs during the main execution.
    """
    try:
        # Load configuration settings
        settings = Settings()

        # Configure logging
        LogSettings(settings.LOG_LEVEL, settings.LOG_FORMAT)

        # Acquire access token
        authenticator = Authenticator(
            settings.CLIENT_ID,
            settings.TENANT_ID,
            settings.THUMBPRINT,
            settings.CERTIFICATE_PATH,
            settings.API_SCOPE,
        )
        access_token = await authenticator.get_access_token()

        # Check if the Excel file already exists
        excel_file_path = f"app/data/{settings.FETCH_FILENAME}"
        if not os.path.exists(excel_file_path):
            # Fetch SharePoint structure
            fetcher = SharePointStructureFetcher(
                access_token,
                settings.ORIGIN_URL,
                settings.PARTIAL_ORIGIN_URL,
                settings.AIOHTTP_LIMIT,
            )
            structure = await fetcher.fetch_structure()

            # Save the structure to an Excel file
            await ExcelExporter.save_structure_to_excel(structure, excel_file_path)
        else:
            logging.info(
                f"Excel file {excel_file_path} already exists. Skipping fetch structure step."
            )

        # Create copy jobs
        copy_jobs_creator = CopyJobsCreator(
            access_token,
            settings.LEVEL,
            settings.DESTINATION_URL,
            settings.BASE_URL,
            settings.AIOHTTP_LIMIT,
            settings.TENANT_NAME,
            settings.IS_MOVE_MODE,
            settings.IGNORE_VERSION_HISTORY,
            settings.ALLOW_SCHEMA_MISMATCH,
            settings.ALLOW_SMALLER_VERSION_LIMIT_ON_DESTINATION,
            settings.INCLUDE_ITEM_PERMISSIONS,
            settings.BYPASS_SHARED_LOCK,
            settings.MOVE_BUT_KEEP_SOURCE,
            settings.EXCLUDE_CHILDREN,
        )
        await copy_jobs_creator.create_copy_jobs()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise MainExecutionError(f"An error occurred during the main execution: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except MainExecutionError as e:
        logging.critical(f"Main execution failed: {e}")
