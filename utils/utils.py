def get_headers(access_token):
    """Get headers for the request."""
    return {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/json'
    }

def get_payload(origin_url, destination_url, is_move_mode):
    """Get payload for the request."""
    return {
        "exportObjectUris": [origin_url],
        "destinationUri": destination_url,
        "options": {
            "IsMoveMode": is_move_mode,
            "IgnoreVersionHistory": False,
            "AllowSchemaMismatch": True,
            "AllowSmallerVersionLimitOnDestination": True,
            "IncludeItemPermissions": False,
            "BypassSharedLock": True,
            "MoveButKeepSource": False,
            "ExcludeChildren": False
        }
    }