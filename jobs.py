import requests
import time
from config import Config

# Function to create copy/move jobs
def create_copy_job(source_url, destination_site, file_paths, access_token):
    url = f"{source_url}/_api/site/CreateCopyJobs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "exportObjectUris": [f"{source_url}{file_path}" for file_path in file_paths],
        "destinationUri": destination_site,
        "options": {
            "IgnoreVersionHistory": True,
            "IsMoveMode": True
        }
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# Function to monitor the progress of jobs
def monitor_job_progress(job_id, source_url, access_token):
    url = f"{source_url}/_api/site/GetCopyJobProgress"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {"JobId": job_id}
    while True:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        progress = response.json()
        print(f"Status do Job: {progress['JobState']}")
        if progress["JobState"] == "Completed":
            print("Job concluído com sucesso!")
            return []  # Sem falhas
        elif progress["JobState"] == "Failed":
            print("Job falhou! Coletando arquivos problemáticos...")
            return progress.get("Errors", [])  # Retorna os arquivos que falharam
        time.sleep(10)  # Wait 10 seconds before checking again

# Function to reprocess failed files
def reprocess_failed_files(failed_files, source_url, destination_site, access_token):
    retries = 0
    while failed_files and retries < Config.MAX_RETRIES:
        retries += 1
        print(f"Tentativa {retries}/{Config.MAX_RETRIES} para reprocessar {len(failed_files)} arquivos...")
        try:
            job_response = create_copy_job(source_url, destination_site, failed_files, access_token)
            job_id = job_response["JobId"]
            failed_files = monitor_job_progress(job_id, source_url, access_token)  # Atualiza os arquivos que falharam
        except Exception as e:
            print(f"Erro durante o reprocessamento: {e}")
    if failed_files:
        print(f"Não foi possível mover os seguintes arquivos após {Config.MAX_RETRIES} tentativas: {failed_files}")
    else:
        print("Todos os arquivos foram movidos com sucesso após reprocessamento.")