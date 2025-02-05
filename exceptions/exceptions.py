class JobCreationError(Exception):
    """Exception raised for errors in the job creation process."""
    pass


class JobMonitoringError(Exception):
    """Exception raised for errors in the job monitoring process."""
    pass


class TokenAcquisitionError(Exception):
    """Exception raised for errors in the token acquisition process."""
    pass
