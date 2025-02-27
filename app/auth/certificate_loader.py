import logging
import os

from app.exceptions import (
    CertificateNotFoundError,
    CertificateReadError,
)


class CertificateLoader:
    """
    A class to handle loading of certificates from a file.

    Methods
    -------
    load_certificate(certificate_path: str) -> str:
        Loads the certificate from the specified file path.
    """

    @staticmethod
    def load_certificate(certificate_path: str) -> str:
        """
        Loads the certificate from the specified file path.

        Args:
            certificate_path (str): The path to the certificate file.

        Returns:
            str: The content of the certificate file.

        Raises:
            CertificateNotFoundError: If the certificate file is not found.
            CertificateReadError: If there is an error reading the certificate file.
        """
        logging.info(f"Loading certificate from path: {certificate_path}")
        if not os.path.exists(certificate_path):
            logging.error("Certificate file not found")
            raise CertificateNotFoundError("Certificate file not found")
        try:
            with open(certificate_path, "r") as cert_file:
                return cert_file.read()
        except Exception as e:
            logging.error(f"Error reading certificate file: {e}")
            raise CertificateReadError(f"Error reading certificate file: {e}")
