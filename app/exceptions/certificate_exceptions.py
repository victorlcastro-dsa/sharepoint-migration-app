class CertificateNotFoundError(Exception):
    """Exception raised when the certificate file is not found."""

    pass


class CertificateReadError(Exception):
    """Exception raised for errors in reading the certificate file."""

    pass
