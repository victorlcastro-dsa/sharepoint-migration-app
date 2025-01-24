import logging
from jobs import SharePointJobManager

if __name__ == "__main__":
    try:
        manager = SharePointJobManager()
        result = manager.create_copy_job(manager.config.ORIGIN_URL, manager.config.DESTINATION_URL)
        job_info = result.get('d', {}).get('CreateCopyJobs', {}).get('results', [{}])[0]
        job_id = job_info.get('JobId')
        job_queue_uri = job_info.get('JobQueueUri')
        encryption_key = job_info.get('EncryptionKey')
        if job_id and job_queue_uri and encryption_key:
            logging.info(f"Job created with ID: {job_id}")
            manager.monitor_job_until_complete(job_id, job_queue_uri, encryption_key)
        else:
            logging.error("Job information not found in the response")
    except Exception as e:
        logging.exception("An error occurred")