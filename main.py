from config import Config
from auth import get_access_token
from sharepoint import list_files_in_folder
from jobs import create_copy_job, monitor_job_progress, reprocess_failed_files

def move_large_folder_in_batches():
    # Get access token
    access_token = get_access_token(Config.TENANT_ID, Config.CLIENT_ID, Config.CLIENT_SECRET)
    print(f"Access Token: {access_token}")

    # List the files in the source folder
    files = list_files_in_folder(Config.SOURCE_URL, access_token)
    print(f"Total de arquivos encontrados: {len(files)}")
    print("Arquivos encontrados:")
    for file in files:
        print(file)

    # Ask user for confirmation
    user_input = input("Deseja continuar com a movimentação dos arquivos? (s/n): ")
    if user_input.lower() != 's':
        print("Movimentação cancelada pelo usuário.")
        return

    # Split the files into batches
    batch_size = 50  # Adjust as needed
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        print(f"Iniciando movimentação do lote: {batch}")
        try:
            # Create job for the current batch
            job_response = create_copy_job(Config.SOURCE_URL, Config.DESTINATION_SITE, batch, access_token)
            job_id = job_response["JobId"]

            # Monitor progress and get failed files
            failed_files = monitor_job_progress(job_id, Config.SOURCE_URL, access_token)

            # Reprocess failed files
            if failed_files:
                reprocess_failed_files(failed_files, Config.SOURCE_URL, Config.DESTINATION_SITE, access_token)
        except Exception as e:
            print(f"Erro ao mover lote {batch}: {e}")

# Execute the script
if __name__ == "__main__":
    move_large_folder_in_batches()