class SharePointAPIError(Exception):
    """Exception raised for errors in SharePoint API requests."""

    pass


class SharePointStructureFetchError(Exception):
    """Exception raised for errors in fetching the SharePoint structure."""

    pass


class SharePointSubfolderFetchError(Exception):
    """Exception raised for errors in fetching the SharePoint subfolders."""

    pass
