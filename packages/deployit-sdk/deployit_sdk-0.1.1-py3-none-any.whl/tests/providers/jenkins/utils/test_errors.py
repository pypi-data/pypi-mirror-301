from datetime import datetime
from unittest.mock import Mock

import pytest
from requests.exceptions import RequestException

from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.utils.errors import (
    JenkinsAPIError,
    JenkinsConnectionError,
    JenkinsError,
)


@pytest.fixture
def mock_presenter():
    return Mock(spec=RichPresenter)


def test_jenkins_error_initialization():
    error = JenkinsError("Test error", "Test details")
    assert str(error).startswith("Test error (Details: Test details, Timestamp:")
    assert isinstance(error.timestamp, datetime)
    assert error.stack_trace is not None


def test_jenkins_error_with_custom_presenter(mock_presenter):
    error = JenkinsError("Test error", "Test details", presenter=mock_presenter)
    assert error.presenter == mock_presenter


def test_jenkins_connection_error():
    error = JenkinsConnectionError("Connection failed")
    assert str(error) == "Connection failed"
    assert isinstance(error, JenkinsError)
    assert isinstance(error, RequestException)


def test_jenkins_api_error(mock_presenter):
    error = JenkinsAPIError("API error", endpoint="/test/endpoint")
    assert str(error).startswith(
        "API error (Details: Endpoint: /test/endpoint, Timestamp:"
    )
    assert isinstance(error, JenkinsError)
    assert isinstance(error, RequestException)


def test_jenkins_error_inheritance():
    assert issubclass(JenkinsConnectionError, JenkinsError)
    assert issubclass(JenkinsConnectionError, RequestException)
    assert issubclass(JenkinsAPIError, JenkinsError)
    assert issubclass(JenkinsAPIError, RequestException)


def test_jenkins_error_with_default_values():
    error = JenkinsError()
    assert str(error).startswith(
        "An error occurred with Jenkins (Details: None, Timestamp:"
    )


def test_jenkins_error_stack_trace():
    try:
        raise ValueError("Test exception")
    except ValueError:
        error = JenkinsError("Test error")
        assert "ValueError: Test exception" in error.stack_trace


def test_jenkins_connection_error_message_property():
    error = JenkinsConnectionError("Test connection error")
    assert error.message == "Test connection error"


def test_jenkins_api_error_custom_message_and_endpoint():
    error = JenkinsAPIError("Custom API error", endpoint="/custom/endpoint")
    assert str(error).startswith(
        "Custom API error (Details: Endpoint: /custom/endpoint, Timestamp:"
    )
