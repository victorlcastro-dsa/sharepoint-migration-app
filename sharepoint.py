import requests

# Function to list files in a folder
def list_files_in_folder(source_url, access_token):
    url = f"{source_url}/_api/web/GetFolderByServerRelativeUrl('{source_url}')/Files"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = response.json()["value"]
    return [file["ServerRelativeUrl"] for file in files]