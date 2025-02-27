import asyncio
import logging
from typing import Any, Dict, List

import aiohttp

from app.exceptions import (
    SharePointStructureFetchError,
    SharePointSubfolderFetchError,
)


class SharePointStructureFetcher:
    """
    A class to fetch the folder structure from a SharePoint site using REST API.

    Attributes:
        access_token (str): The access token for SharePoint API.
        origin_url (str): The origin URL of the SharePoint site.
        partial_origin_url (str): The partial URL of the SharePoint site.
        aiohttp_limit (int): The connection limit for aiohttp.
    """

    def __init__(
        self,
        access_token: str,
        origin_url: str,
        partial_origin_url: str,
        aiohttp_limit: int,
    ) -> None:
        """
        Initializes the SharePointStructureFetcher instance with access token and origin URL.
        """
        self.access_token = access_token
        self.origin_url = origin_url
        self.partial_origin_url = partial_origin_url
        self.aiohttp_limit = aiohttp_limit

    async def fetch_structure(self) -> Dict[str, Any]:
        """
        Fetches the folder structure from the SharePoint site.

        Returns:
            Dict[str, Any]: The folder structure.

        Raises:
            SharePointStructureFetchError: If there is an error fetching the folder structure.
        """
        url = f"{self.origin_url}/_api/web/GetFolderByServerRelativeUrl('{self.partial_origin_url}')?$expand=Folders"
        logging.info(f"Fetching structure from {url}")
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json;odata=verbose",
        }

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=self.aiohttp_limit)
        ) as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logging.error(
                            f"Failed to fetch structure: {response.status} - {error_text}"
                        )
                        raise SharePointStructureFetchError(
                            f"Failed to fetch structure: {response.status} - {error_text}"
                        )
                    structure = await response.json()
            except aiohttp.ClientError as e:
                logging.error(f"HTTP request failed: {e}")
                raise SharePointStructureFetchError(f"HTTP request failed: {e}")

        folders = structure.get("d", {}).get("Folders", {}).get("results", [])
        structure["d"]["Folders"]["results"] = await self._extract_folders_from_api(
            folders
        )

        return structure

    async def _extract_folders_from_api(
        self, folders: List[Dict[str, Any]], parent_path: str = "", level: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Recursively extracts folder information from the API response.

        Args:
            folders (List[Dict[str, Any]]): The list of folders to extract.
            parent_path (str): The parent path for the current folders.
            level (int): The level of the current folders.

        Returns:
            List[Dict[str, Any]]: The extracted folder information.
        """
        data = []
        tasks = []
        for folder in folders:
            folder_path = f"{parent_path}/{folder['Name']}".strip("/")
            folder_info = {
                "Name": folder["Name"],
                "Path": folder_path,
                "ParentFolder": parent_path,
                "Level": level,
                "TimeCreated": folder["TimeCreated"],
                "TimeLastModified": folder["TimeLastModified"],
                "ItemCount": folder["ItemCount"],
                "ServerRelativeUrl": folder["ServerRelativeUrl"],
                "UniqueId": folder["UniqueId"],
            }
            data.append(folder_info)
            tasks.append(
                self._fetch_and_extract_subfolders(
                    folder["ServerRelativeUrl"], folder_path, level + 1
                )
            )

        subfolders_data = await asyncio.gather(*tasks)
        for subfolder in subfolders_data:
            data.extend(subfolder)

        return data

    async def _fetch_and_extract_subfolders(
        self, folder_url: str, parent_path: str, level: int
    ) -> List[Dict[str, Any]]:
        """
        Fetches and extracts subfolders from a given folder URL.

        Args:
            folder_url (str): The URL of the folder to fetch subfolders from.
            parent_path (str): The parent path for the current folders.
            level (int): The level of the current folders.

        Returns:
            List[Dict[str, Any]]: The extracted subfolder information.
        """
        subfolders = await self._fetch_subfolders(folder_url)
        return await self._extract_folders_from_api(subfolders, parent_path, level)

    async def _fetch_subfolders(self, folder_url: str) -> List[Dict[str, Any]]:
        """
        Fetches the subfolders from a given folder URL.

        Args:
            folder_url (str): The URL of the folder to fetch subfolders from.

        Returns:
            List[Dict[str, Any]]: The list of subfolders.

        Raises:
            SharePointSubfolderFetchError: If there is an error fetching the subfolders.
        """
        url = f"{self.origin_url}/_api/web/GetFolderByServerRelativeUrl('{folder_url}')/Folders"
        logging.info(f"Fetching subfolders from {url}")
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json;odata=verbose",
        }

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=self.aiohttp_limit)
        ) as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logging.error(
                            f"Failed to fetch subfolders: {response.status} - {error_text}"
                        )
                        raise SharePointSubfolderFetchError(
                            f"Failed to fetch subfolders: {response.status} - {error_text}"
                        )
                    subfolders = await response.json()
            except aiohttp.ClientError as e:
                logging.error(f"HTTP request failed: {e}")
                raise SharePointSubfolderFetchError(f"HTTP request failed: {e}")

        return subfolders.get("d", {}).get("results", [])
