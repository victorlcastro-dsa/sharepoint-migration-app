import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List

import pandas as pd

from app.exceptions import ExcelWriteError


class ExcelExporter:
    """
    A class to handle exporting SharePoint folder structure to an Excel file.

    Methods
    -------
    save_structure_to_excel(structure: Dict[str, Any], file_path: str) -> None:
        Saves the SharePoint folder structure to an Excel file.
    """

    @staticmethod
    async def save_structure_to_excel(
        structure: Dict[str, Any], file_path: str
    ) -> None:
        """
        Saves the SharePoint folder structure to an Excel file.

        Args:
            structure (Dict[str, Any]): The folder structure.
            file_path (str): The path to the Excel file.

        Raises:
            ExcelWriteError: If there is an error writing the Excel file.
        """
        logging.info(f"Starting to save SharePoint structure to {file_path}")
        try:
            folders = structure.get("d", {}).get("Folders", {}).get("results", [])
            all_folders_data = ExcelExporter._extract_folders_for_excel(folders)

            all_folders_df = pd.DataFrame(all_folders_data)

            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as pool:
                await loop.run_in_executor(
                    pool, ExcelExporter._write_to_excel, all_folders_df, file_path
                )

            logging.info(f"Successfully saved SharePoint structure to {file_path}")
        except Exception as e:
            logging.error(f"Failed to save SharePoint structure to {file_path}: {e}")
            raise ExcelWriteError(
                f"Failed to save SharePoint structure to {file_path}: {e}"
            )

    @staticmethod
    def _write_to_excel(df: pd.DataFrame, file_path: str) -> None:
        """
        Writes the DataFrame to an Excel file.

        Args:
            df (pd.DataFrame): The DataFrame to write.
            file_path (str): The path to the Excel file.
        """
        with pd.ExcelWriter(file_path) as writer:
            df.to_excel(writer, index=False, sheet_name="Folders")

    @staticmethod
    def _extract_folders_for_excel(
        folders: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Extracts folder information for saving to Excel.

        Args:
            folders (List[Dict[str, Any]]): The list of folders to extract.

        Returns:
            List[Dict[str, Any]]: The extracted folder information.
        """
        data = []
        for folder in folders:
            data.append(
                {
                    "Name": folder["Name"],
                    "Path": folder["Path"],
                    "ParentFolder": folder["ParentFolder"],
                    "Level": folder["Level"],
                    "TimeCreated": folder["TimeCreated"],
                    "TimeLastModified": folder["TimeLastModified"],
                    "ItemCount": folder["ItemCount"],
                    "ServerRelativeUrl": folder["ServerRelativeUrl"],
                    "UniqueId": folder["UniqueId"],
                }
            )
        return data
