import requests
import logging
import time
from auth import get_access_token
from config import Config

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_copy_job(origin_url, destination_url, is_move_mode=False):
    logging.info("Starting job creation process")
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
        logging.info("Job creation successful")
        job_response = response.json()
        logging.info(f"Job response: {job_response}")
        return job_response
    else:
        logging.error(f"Failed to create copy job: {response.status_code} - {response.text}")
        raise Exception(f"Failed to create copy job: {response.status_code} - {response.text}")

def monitor_job(job_id):
    logging.info(f"Starting job monitoring for job ID: {job_id}")
    access_token = get_access_token(Config.TENANT_ID, Config.CLIENT_ID, Config.CERTIFICATE_PATH)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json;odata=verbose'
    }

    response = requests.get(
        f"https://{Config.TENANT_NAME}.sharepoint.com/_api/site/GetCopyJobProgress(jobId='{job_id}')",
        headers=headers
    )

    if response.status_code == 200:
        job_status = response.json()
        logging.info(f"Job status: {job_status}")
        return job_status
    else:
        logging.error(f"Failed to monitor job: {response.status_code} - {response.text}")
        raise Exception(f"Failed to monitor job: {response.status_code} - {response.text}")

def monitor_job_until_complete(job_id, interval=60, initial_delay=10):
    logging.info(f"Initial delay of {initial_delay} seconds before starting job monitoring")
    time.sleep(initial_delay)
    while True:
        job_status = monitor_job(job_id)
        status = job_status.get('d', {}).get('JobState')
        if status == 'Completed':
            logging.info(f"Job {job_id} completed successfully")
            break
        elif status == 'Failed':
            logging.error(f"Job {job_id} failed")
            break
        else:
            logging.info(f"Job {job_id} is still in progress. Status: {status}")
            time.sleep(interval)

if __name__ == "__main__":
    try:
        result = create_copy_job(Config.ORIGIN_URL, Config.DESTINATION_URL, is_move_mode=True)
        job_id = result.get('d', {}).get('CreateCopyJobs', {}).get('results', [{}])[0].get('JobId')
        if job_id:
            logging.info(f"Job created with ID: {job_id}")
            monitor_job_until_complete(job_id)
        else:
            logging.error("Job ID not found in the response")
    except Exception as e:
        logging.exception("An error occurred")