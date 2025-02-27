import asyncio
import logging
import urllib.parse
from typing import Any, Dict, List

import aiohttp
import pandas as pd

from app.exceptions import (
    ExcelReadError,
    JobCreationError,
    SharePointAPIError,
)


class CopyJobsCreator:
    def __init__(
        self,
        access_token: str,
        level: int,
        destination_url: str,
        base_url: str,
        aiohttp_limit: int,
        tenant_name: str,
        is_move_mode: bool,
        ignore_version_history: bool,
        allow_schema_mismatch: bool,
        allow_smaller_version_limit_on_destination: bool,
        include_item_permissions: bool,
        bypass_shared_lock: bool,
        move_but_keep_source: bool,
        exclude_children: bool,
    ) -> None:
        """
        Initializes the CopyJobsCreator instance.

        Args:
            settings (Settings): The settings instance containing configuration.
            access_token (str): The access token for authentication.
            level (int): The level of items to create copy jobs for.
            destination_url (str): The destination URL for the copy jobs.
        """
        self.access_token = access_token
        self.level = level
        self.destination_url = destination_url
        self.base_url = base_url
        self.aiohttp_limit = aiohttp_limit
        self.tenant_name = tenant_name
        self.is_move_mode = is_move_mode
        self.ignore_version_history = ignore_version_history
        self.allow_schema_mismatch = allow_schema_mismatch
        self.allow_smaller_version_limit_on_destination = (
            allow_smaller_version_limit_on_destination
        )
        self.include_item_permissions = include_item_permissions
        self.bypass_shared_lock = bypass_shared_lock
        self.move_but_keep_source = move_but_keep_source
        self.exclude_children = exclude_children

    async def create_copy_jobs(self) -> List[Dict[str, Any]]:
        """
        Create copy jobs in SharePoint for items with the specified level.

        Returns:
            List[Dict[str, Any]]: A list of responses from the job creation requests.

        Raises:
            ExcelReadError: If there is an error reading the Excel file.
            SharePointAPIError: If there is an error with the SharePoint API request.
            JobCreationError: If there is an error creating the copy jobs.
        """
        logging.info(f"Starting job creation process for items with Level {self.level}")
        headers = self._get_headers()
        jobs = []

        # Load data from Excel
        try:
            df = pd.read_excel(
                "app/data/sharepoint_folder_structure.xlsx", sheet_name="Folders"
            )
        except Exception as e:
            logging.error(f"Failed to read Excel file: {e}")
            raise ExcelReadError(f"Failed to read Excel file: {e}")

        origin_urls = [
            urllib.parse.quote(f"{self.base_url}{row['ServerRelativeUrl']}", safe=":/%")
            for _, row in df.iterrows()
            if row["Level"] == self.level
        ]

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=self.aiohttp_limit)
        ) as session:
            tasks = [
                self._create_job(session, headers, origin_url)
                for origin_url in origin_urls
            ]
            job_responses = await asyncio.gather(*tasks, return_exceptions=True)

        for response in job_responses:
            if isinstance(response, Exception):
                logging.error(f"Job creation failed: {response}")
                raise JobCreationError(f"Job creation failed: {response}")
            jobs.append(response)

        logging.info(f"Created {len(jobs)} copy jobs for level {self.level}")
        return jobs

    async def _create_job(
        self, session: aiohttp.ClientSession, headers: Dict[str, str], origin_url: str
    ) -> Dict[str, Any]:
        """
        Create a single copy job in SharePoint.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            headers (Dict[str, str]): The headers for the request.
            origin_url (str): The origin URL for the copy job.

        Returns:
            Dict[str, Any]: The response from the job creation request.

        Raises:
            SharePointAPIError: If there is an error with the SharePoint API request.
        """
        payload = self._get_payload(origin_url, self.destination_url)
        try:
            async with session.post(
                f"https://{self.tenant_name}.sharepoint.com/_api/site/CreateCopyJobs",
                headers=headers,
                json=payload,
            ) as response:
                response_text = await response.text()
                if response.status == 200:
                    logging.info(f"Job creation successful for {origin_url}")
                    return await response.json()
                else:
                    logging.error(
                        f"Failed to create copy job for {origin_url}: {response.status} - {response_text}"
                    )
                    raise SharePointAPIError(
                        f"Failed to create copy job for {origin_url}: {response.status} - {response_text}"
                    )
        except aiohttp.ClientError as e:
            logging.error(f"HTTP request failed: {e}")
            raise SharePointAPIError(f"HTTP request failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise SharePointAPIError(f"Unexpected error: {e}")

    def _get_headers(self) -> Dict[str, str]:
        """
        Get headers for the request.

        Returns:
            Dict[str, str]: The headers for the request.
        """
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json;odata=verbose",
            "Content-Type": "application/json",
        }

    def _get_payload(self, origin_url: str, destination_url: str) -> Dict[str, Any]:
        """
        Get payload for the request.

        Args:
            origin_url (str): The origin URL for the copy job.
            destination_url (str): The destination URL for the copy job.

        Returns:
            Dict[str, Any]: The payload for the request.
        """
        return {
            "exportObjectUris": [origin_url],
            "destinationUri": urllib.parse.quote(destination_url, safe=":/%"),
            "options": {
                "IsMoveMode": self.is_move_mode,
                "IgnoreVersionHistory": self.ignore_version_history,
                "AllowSchemaMismatch": self.allow_schema_mismatch,
                "AllowSmallerVersionLimitOnDestination": self.allow_smaller_version_limit_on_destination,
                "IncludeItemPermissions": self.include_item_permissions,
                "BypassSharedLock": self.bypass_shared_lock,
                "MoveButKeepSource": self.move_but_keep_source,
                "ExcludeChildren": self.exclude_children,
            },
        }
