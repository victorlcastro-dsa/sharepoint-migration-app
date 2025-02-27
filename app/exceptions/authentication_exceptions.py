class TokenAcquisitionError(Exception):
    """Exception raised for errors in the token acquisition process."""

    pass


class MSALAuthenticationError(Exception):
    """Exception raised for errors in the MSAL authentication process."""

    pass
