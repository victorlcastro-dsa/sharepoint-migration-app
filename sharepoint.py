import requests

# Function to list files in a folder
def list_files_in_folder(source_url, folder_path, access_token):
    # Ensure the folder path starts with a slash
    if not folder_path.startswith('/'):
        folder_path = '/' + folder_path

    # Encode the folder path
    encoded_folder_path = requests.utils.quote(folder_path)

    url = f"{source_url}/_api/web/GetFolderByServerRelativeUrl('{encoded_folder_path}')/Files"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    print(response.content)
    response.raise_for_status()
    files = response.json()["value"]
    return [file["ServerRelativeUrl"] for file in files]