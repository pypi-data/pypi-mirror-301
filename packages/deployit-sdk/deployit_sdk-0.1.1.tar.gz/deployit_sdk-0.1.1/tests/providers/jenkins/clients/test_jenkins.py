from unittest.mock import Mock, patch

import pytest

from deployit.providers.jenkins.clients.http import HTTPClient
from deployit.providers.jenkins.clients.jenkins import JenkinsAPIClient
from deployit.providers.jenkins.models.url import JenkinsURLBuilder
from deployit.providers.jenkins.utils.errors import JenkinsConnectionError


@pytest.fixture
def url_builder():
    return Mock(spec=JenkinsURLBuilder)


@pytest.fixture
def http_client():
    return Mock(spec=HTTPClient)


@pytest.fixture
def jenkins_client(url_builder, http_client):
    return JenkinsAPIClient(url_builder, http_client)


def test_jenkins_api_client_initialization(jenkins_client, url_builder, http_client):
    assert jenkins_client.url_builder == url_builder
    assert jenkins_client.http_client == http_client


@pytest.mark.parametrize(
    "method, expected_method",
    [
        ("GET", "get"),
        ("POST", "post"),
        ("PUT", "put"),
        ("DELETE", "delete"),
    ],
)
def test_make_request_valid_methods(
    jenkins_client, url_builder, http_client, method, expected_method
):
    url_builder.build_url.return_value = "http://jenkins.example.com/api/endpoint"
    getattr(http_client, expected_method).return_value = {"key": "value"}

    result = jenkins_client.make_request("api/endpoint", method=method)

    url_builder.build_url.assert_called_once_with("api/endpoint")
    if method == "GET":
        getattr(http_client, expected_method).assert_called_once_with(
            "http://jenkins.example.com/api/endpoint", headers={}, is_json=True
        )
    elif method == "DELETE":
        getattr(http_client, expected_method).assert_called_once_with(
            "http://jenkins.example.com/api/endpoint", headers={}, is_json=True
        )
    else:
        getattr(http_client, expected_method).assert_called_once_with(
            "http://jenkins.example.com/api/endpoint",
            headers={},
            data=None,
            is_json=True,
        )
    assert result == {"key": "value"}


def test_make_request_invalid_method(jenkins_client):
    with pytest.raises(ValueError, match="Unsupported method: INVALID"):
        jenkins_client.make_request("api/endpoint", method="INVALID")


def test_make_request_with_custom_headers(jenkins_client, url_builder, http_client):
    url_builder.build_url.return_value = "http://jenkins.example.com/api/endpoint"
    http_client.get.return_value = {"key": "value"}
    custom_headers = {"X-Custom-Header": "CustomValue"}

    result = jenkins_client.make_request("api/endpoint", headers=custom_headers)

    url_builder.build_url.assert_called_once_with("api/endpoint")
    http_client.get.assert_called_once_with(
        "http://jenkins.example.com/api/endpoint", headers=custom_headers, is_json=True
    )
    assert result == {"key": "value"}


def test_make_request_with_additional_kwargs(jenkins_client, url_builder, http_client):
    url_builder.build_url.return_value = "http://jenkins.example.com/api/endpoint"
    http_client.get.return_value = {"key": "value"}

    result = jenkins_client.make_request(
        "api/endpoint", job_name="test-job", build_number=42
    )

    url_builder.build_url.assert_called_once_with(
        "api/endpoint", job_name="test-job", build_number=42
    )
    http_client.get.assert_called_once_with(
        "http://jenkins.example.com/api/endpoint", headers={}, is_json=True
    )
    assert result == {"key": "value"}


def test_make_request_http_client_error(jenkins_client, url_builder, http_client):
    url_builder.build_url.return_value = "http://jenkins.example.com/api/endpoint"
    http_client.get.side_effect = JenkinsConnectionError("Connection failed")

    with pytest.raises(JenkinsConnectionError, match="Connection failed"):
        jenkins_client.make_request("api/endpoint")


def test_make_request_url_builder_error(jenkins_client, url_builder):
    url_builder.build_url.side_effect = KeyError("Missing parameter")

    with pytest.raises(KeyError, match="Missing parameter"):
        jenkins_client.make_request("api/endpoint")


def test_make_request_non_json_response(jenkins_client, url_builder, http_client):
    url_builder.build_url.return_value = "http://jenkins.example.com/api/endpoint"
    http_client.get.return_value = {"content": "Non-JSON content"}

    result = jenkins_client.make_request("api/endpoint", is_json=False)

    assert result == {"content": "Non-JSON content"}
    http_client.get.assert_called_once_with(
        "http://jenkins.example.com/api/endpoint", headers={}, is_json=False
    )
