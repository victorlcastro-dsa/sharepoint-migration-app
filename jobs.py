import requests
import logging
import time
from auth import get_access_token
from config import Config
from exceptions import JobCreationError, JobMonitoringError
from logging_config import setup_logging

setup_logging()

def create_copy_job(origin_url, destination_url, is_move_mode=False):
    """Create a copy job in SharePoint."""
    logging.info("Starting job creation process")
    access_token = get_access_token()
    headers = _get_headers(access_token)
    payload = _get_payload(origin_url, destination_url, is_move_mode)

    response = requests.post(
        f"https://{Config().TENANT_NAME}.sharepoint.com/_api/site/CreateCopyJobs",
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
        raise JobCreationError(f"Failed to create copy job: {response.status_code} - {response.text}")

def _get_headers(access_token):
    """Get headers for the request."""
    return {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/json'
    }

def _get_payload(origin_url, destination_url, is_move_mode):
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

def monitor_job(job_id, job_queue_uri, encryption_key):
    """Monitor the status of a copy job."""
    logging.info(f"Starting job monitoring for job ID: {job_id}")
    access_token = get_access_token()
    headers = _get_headers(access_token)

    # URL da API para obter o progresso do job
    url = f"https://{Config().TENANT_NAME}.sharepoint.com/_api/site/GetCopyJobProgress"

    # Payload JSON com as informações do job
    payload = {
        "copyJobInfo": {
            "JobId": job_id,
            "JobQueueUri": job_queue_uri,
            "EncryptionKey": encryption_key
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        job_status = response.json()
        logging.info(f"Job status: {job_status}")
        return job_status
    else:
        logging.error(f"Failed to monitor job: {response.status_code} - {response.text}")
        raise JobMonitoringError(f"Failed to monitor job: {response.status_code} - {response.text}")

def monitor_job_until_complete(job_id, job_queue_uri, encryption_key, interval=60, initial_delay=10, max_initial_wait=120):
    """Monitor the job until it is complete or the maximum initial wait time is reached."""
    logging.info(f"Initial delay of {initial_delay} seconds before starting job monitoring")
    time.sleep(initial_delay)
    start_time = time.time()
    job_found = False

    while time.time() - start_time < max_initial_wait:
        try:
            job_status = monitor_job(job_id, job_queue_uri, encryption_key)
            job_found = True
            break
        except JobMonitoringError:
            logging.warning(f"Job ID {job_id} not found, retrying...")
            time.sleep(interval)

    if not job_found:
        logging.error(f"Job ID {job_id} not found after {max_initial_wait} seconds")
        raise JobMonitoringError(f"Job ID {job_id} not found after {max_initial_wait} seconds")

    while True:
        job_status = monitor_job(job_id, job_queue_uri, encryption_key)
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
        config = Config()
        result = create_copy_job(config.ORIGIN_URL, config.DESTINATION_URL, is_move_mode=False)
        job_info = result.get('d', {}).get('CreateCopyJobs', {}).get('results', [{}])[0]
        job_id = job_info.get('JobId')
        job_queue_uri = job_info.get('JobQueueUri')
        encryption_key = job_info.get('EncryptionKey')
        if job_id and job_queue_uri and encryption_key:
            logging.info(f"Job created with ID: {job_id}")
            monitor_job_until_complete(job_id, job_queue_uri, encryption_key)
        else:
            logging.error("Job information not found in the response")
    except Exception as e:
        logging.exception("An error occurred")