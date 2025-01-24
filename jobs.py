import requests
from auth import get_access_token
from config import Config

def create_copy_job(origin_url, destination_url, is_move_mode=False):
    access_token = get_access_token(Config.TENANT_ID, Config.CLIENT_ID, Config.CERTIFICATE_PATH)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/json'
    }

    payload = {
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

    response = requests.post(
        f"https://{Config.TENANT_NAME}.sharepoint.com/_api/site/CreateCopyJobs",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to create copy job: {response.status_code} - {response.text}")

if __name__ == "__main__":
    result = create_copy_job(Config.ORIGIN_URL, Config.DESTINATION_URL, is_move_mode=True)
    print(result)