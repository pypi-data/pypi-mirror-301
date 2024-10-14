import datetime
import traceback

from requests.exceptions import RequestException

from deployit.providers.jenkins.presentation.rich import RichPresenter


class JenkinsError(Exception):
    """
    Base exception class for Jenkins-related errors.
    """

    def __init__(
        self,
        message="An error occurred with Jenkins",
        details=None,
        presenter=RichPresenter(),
    ):
        super().__init__(message)
        self.details = details
        self.timestamp = datetime.datetime.now()
        self.stack_trace = traceback.format_exc()
        self.presenter = presenter

    def __str__(self):
        return f"{super().__str__()} (Details: {self.details}, Timestamp: {self.timestamp})"


class JenkinsConnectionError(JenkinsError, RequestException):
    """
    Raised when there is a connection error with Jenkins.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class JenkinsAPIError(JenkinsError, RequestException):
    """
    Raised when there is a general API error with Jenkins.
    """

    def __init__(self, message="An API error occurred with Jenkins", endpoint=None):
        details = f"Endpoint: {endpoint}"
        super().__init__(message, details)
        self.presenter.display_error(
            f"JenkinsAPIError: {message} (Endpoint: {endpoint})"
        )
