class nexussException(Exception):
    """Base exception for this script.

    :note: This exception should not be raised directly."""
    pass


class QueryReturnedBadRequestException(nexussException):
    pass


class QueryReturnedForbiddenException(nexussException):
    pass


class ProfileNotExistsException(nexussException):
    pass


class ProfileHasNoPicsException(nexussException):
    """
    .. deprecated:: 4.2.2
       Not raised anymore.
    """
    pass


class PrivateProfileNotFollowedException(nexussException):
    pass


class LoginRequiredException(nexussException):
    pass


class LoginException(nexussException):
    pass


class TwoFactorAuthRequiredException(LoginException):
    pass


class InvalidArgumentException(nexussException):
    pass


class BadResponseException(nexussException):
    pass


class BadCredentialsException(LoginException):
    pass


class ConnectionException(nexussException):
    pass


class PostChangedException(nexussException):
    """.. versionadded:: 4.2.2"""
    pass


class QueryReturnedNotFoundException(ConnectionException):
    pass


class TooManyRequestsException(ConnectionException):
    pass

class IPhoneSupportDisabledException(nexussException):
    pass

class AbortDownloadException(Exception):
    """
    Exception that is not catched in the error catchers inside the download loop and so aborts the
    download loop.

    This exception is not a subclass of ``nexussException``.

    .. versionadded:: 4.7
    """
    pass
