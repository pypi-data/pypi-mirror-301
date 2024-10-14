from unittest.mock import MagicMock, patch

import pytest
import requests

from deployit.providers.jenkins.clients.http import RequestsHTTPClient
from deployit.providers.jenkins.utils.config import Config
from deployit.providers.jenkins.utils.errors import JenkinsConnectionError


@pytest.fixture
def http_client():
    with patch("deployit.providers.jenkins.clients.http.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "crumbRequestField": "Jenkins-Crumb",
            "crumb": "test-crumb",
        }
        mock_get.return_value = mock_response
        client = RequestsHTTPClient()
        yield client


def test_init(http_client):
    assert isinstance(http_client, RequestsHTTPClient)
    assert http_client._base_header["Jenkins-Crumb"] == "test-crumb"


@pytest.mark.parametrize(
    "method,http_method",
    [
        ("get", "get"),
        ("post", "post"),
        ("delete", "delete"),
        ("put", "put"),
    ],
)
def test_http_methods(http_client, method, http_method):
    with patch(
        f"deployit.providers.jenkins.clients.http.requests.{http_method}"
    ) as mock_method:
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_method.return_value = mock_response

        url = "http://example.com"
        headers = {"Custom-Header": "Value"}
        data = {"data": "test"} if method in ["post", "put"] else None

        if method in ["post", "put"]:
            result = getattr(http_client, method)(url, headers=headers, data=data)
        else:
            result = getattr(http_client, method)(url, headers=headers)

        expected_headers = {**http_client._base_header, **headers}
        if method in ["post", "put"]:
            mock_method.assert_called_once_with(
                url, headers=expected_headers, data=data, timeout=Config.TIMEOUT
            )
        else:
            mock_method.assert_called_once_with(
                url, headers=expected_headers, timeout=Config.TIMEOUT
            )
        assert result == {"key": "value"}


@pytest.mark.parametrize("method", ["get", "post", "delete", "put"])
def test_http_methods_error(http_client, method):
    with patch(
        f"deployit.providers.jenkins.clients.http.requests.{method}"
    ) as mock_method:
        mock_method.side_effect = requests.exceptions.RequestException("Test error")

        url = "http://example.com"
        with pytest.raises(JenkinsConnectionError) as exc_info:
            if method in ["post", "put"]:
                getattr(http_client, method)(url, data={})
            else:
                getattr(http_client, method)(url)

        assert str(exc_info.value) == f"{method.upper()} request failed: Test error"


def test_get_method_not_json(http_client):
    with patch("deployit.providers.jenkins.clients.http.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response._content = b"Not JSON content"
        mock_get.return_value = mock_response

        result = http_client.get("http://example.com", is_json=False)
        assert result == {"content": "Not JSON content"}


def test_post_method_response(http_client):
    with patch("deployit.providers.jenkins.clients.http.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        result = http_client.post("http://example.com")
        assert result == {"status": "success"}


def test_set_base_header_error():
    with patch("deployit.providers.jenkins.clients.http.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        with patch("builtins.print") as mock_print:
            RequestsHTTPClient()
            mock_print.assert_called_once_with(
                "An error occurred, verify your environment variables if they are setted correctly: Connection error"
            )


def test_get_method_with_custom_timeout(http_client):
    with patch("deployit.providers.jenkins.clients.http.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        custom_timeout = 30
        Config.TIMEOUT = custom_timeout

        http_client.get("http://example.com")

        mock_get.assert_called_once_with(
            "http://example.com",
            headers=http_client._base_header,
            timeout=custom_timeout,
        )


def test_post_method_with_empty_data(http_client):
    with patch("deployit.providers.jenkins.clients.http.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        result = http_client.post("http://example.com", data={})

        mock_post.assert_called_once_with(
            "http://example.com",
            headers=http_client._base_header,
            data={},
            timeout=Config.TIMEOUT,
        )
        assert result == {"status": "success"}


def test_delete_method_with_response_error(http_client):
    with patch(
        "deployit.providers.jenkins.clients.http.requests.delete"
    ) as mock_delete:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error"
        )
        mock_delete.return_value = mock_response

        with pytest.raises(JenkinsConnectionError) as exc_info:
            http_client.delete("http://example.com")

        assert "DELETE request failed: 404 Client Error" in str(exc_info.value)


def test_put_method_with_large_data(http_client):
    with patch("deployit.providers.jenkins.clients.http.requests.put") as mock_put:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_put.return_value = mock_response

        large_data = {"key": "x" * 1000000}  # 1MB of data
        result = http_client.put("http://example.com", data=large_data)

        mock_put.assert_called_once_with(
            "http://example.com",
            headers=http_client._base_header,
            data=large_data,
            timeout=Config.TIMEOUT,
        )
        assert result == {"status": "success"}


def test_post_method_with_custom_headers(http_client):
    with patch("deployit.providers.jenkins.clients.http.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        custom_headers = {"X-Custom-Header": "CustomValue"}
        result = http_client.post("http://example.com", headers=custom_headers)

        expected_headers = {**http_client._base_header, **custom_headers}
        mock_post.assert_called_once_with(
            "http://example.com",
            headers=expected_headers,
            data=None,
            timeout=Config.TIMEOUT,
        )
        assert result == {"status": "success"}


def test_init_with_network_error():
    with patch("deployit.providers.jenkins.clients.http.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with patch("builtins.print") as mock_print:
            client = RequestsHTTPClient()
            mock_print.assert_called_once_with(
                "An error occurred, verify your environment variables if they are setted correctly: Network error"
            )
            assert not hasattr(client, "_base_header")
