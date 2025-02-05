import aiohttp
import logging
import time
import asyncio
from auth import get_access_token
from config import Config
from exceptions import JobCreationError, JobMonitoringError
from log_config import setup_logging
from utils import get_headers, get_payload

setup_logging()


class SharePointJobManager:
    def __init__(self):
        self.config = Config()

    async def create_copy_job(self, origin_url, destination_url):
        """Create a copy job in SharePoint."""
        logging.info("Starting job creation process")
        access_token = await get_access_token()
        headers = get_headers(access_token)
        payload = get_payload(origin_url, destination_url)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://{self.config.TENANT_NAME}.sharepoint.com/_api/site/CreateCopyJobs",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    logging.info("Job creation successful")
                    job_response = await response.json()
                    logging.info(f"Job response: {job_response}")
                    return job_response
                else:
                    logging.error(f"Failed to create copy job: {
                                  response.status} - {response.text}")
                    raise JobCreationError(f"Failed to create copy job: {
                                           response.status} - {response.text}")

    async def monitor_job(self, job_id, job_queue_uri, encryption_key):
        """Monitor the status of a copy job."""
        logging.info(f"Starting job monitoring for job ID: {job_id}")
        access_token = await get_access_token()
        headers = get_headers(access_token)

        url = f"https://{self.config.TENANT_NAME}.sharepoint.com/_api/site/GetCopyJobProgress"
        payload = {
            "copyJobInfo": {
                "JobId": job_id,
                "JobQueueUri": job_queue_uri,
                "EncryptionKey": encryption_key
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    job_status = await response.json()
                    logging.info(f"Job status: {job_status}")
                    return job_status
                else:
                    logging.error(f"Failed to monitor job: {
                                  response.status} - {response.text}")
                    raise JobMonitoringError(f"Failed to monitor job: {
                                             response.status} - {response.text}")

    async def monitor_job_until_complete(self, job_id, job_queue_uri, encryption_key, interval=None, initial_delay=None, max_initial_wait=None):
        """Monitor the job until it is complete or the maximum initial wait time is reached."""
        interval = interval or self.config.INTERVAL
        initial_delay = initial_delay or self.config.INITIAL_DELAY
        max_initial_wait = max_initial_wait or self.config.MAX_INITIAL_WAIT

        logging.info(f"Initial delay of {
                     initial_delay} seconds before starting job monitoring")
        await asyncio.sleep(initial_delay)
        start_time = time.time()
        job_found = False

        while time.time() - start_time < max_initial_wait:
            try:
                job_status = await self.monitor_job(job_id, job_queue_uri, encryption_key)
                job_found = True
                break
            except JobMonitoringError:
                logging.warning(f"Job ID {job_id} not found, retrying...")
                await asyncio.sleep(interval)

        if not job_found:
            logging.error(f"Job ID {job_id} not found after {
                          max_initial_wait} seconds")
            raise JobMonitoringError(f"Job ID {job_id} not found after {
                                     max_initial_wait} seconds")

        while True:
            job_status = await self.monitor_job(job_id, job_queue_uri, encryption_key)
            status = job_status.get('d', {}).get('JobState')
            if status == 'Completed':
                logging.info(f"Job {job_id} completed successfully")
                break
            elif status == 'Failed':
                logging.error(f"Job {job_id} failed")
                break
            else:
                logging.info(
                    f"Job {job_id} is still in progress. Status: {status}")
                await asyncio.sleep(interval)
