from config import Config


def get_headers(access_token):
    """Get headers for the request."""
    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json",
    }


def get_payload(origin_url, destination_url):
    """Get payload for the request."""
    config = Config()
    return {
        "exportObjectUris": [origin_url],
        "destinationUri": destination_url,
        "options": {
            "IsMoveMode": config.IS_MOVE_MODE,
            "IgnoreVersionHistory": config.IGNORE_VERSION_HISTORY,
            "AllowSchemaMismatch": config.ALLOW_SCHEMA_MISMATCH,
            "AllowSmallerVersionLimitOnDestination": config.ALLOW_SMALLER_VERSION_LIMIT_ON_DESTINATION,
            "IncludeItemPermissions": config.INCLUDE_ITEM_PERMISSIONS,
            "BypassSharedLock": config.BYPASS_SHARED_LOCK,
            "MoveButKeepSource": config.MOVE_BUT_KEEP_SOURCE,
            "ExcludeChildren": config.EXCLUDE_CHILDREN,
        },
    }
