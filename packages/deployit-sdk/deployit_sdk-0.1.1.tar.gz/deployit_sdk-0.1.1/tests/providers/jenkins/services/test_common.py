from unittest.mock import Mock, patch

import pytest

from deployit.providers.jenkins.endpoints.common import CommonEndpoints
from deployit.providers.jenkins.services.common import JenkinsCommonApiService
from deployit.providers.jenkins.utils.errors import JenkinsError


@pytest.fixture
def mock_jenkins_client():
    return Mock()


@pytest.fixture
def common_service(mock_jenkins_client):
    return JenkinsCommonApiService(mock_jenkins_client)


def test_get_jenkins_info_success(common_service):
    expected_response = {"version": "2.303.3", "nodes": 5}
    common_service.jenkins_client.make_request.return_value = expected_response

    result = common_service.get_jenkins_info()

    assert result == expected_response
    common_service.jenkins_client.make_request.assert_called_once_with(
        CommonEndpoints.INFO, method="GET"
    )


def test_get_jenkins_info_jenkins_error(common_service):
    common_service.jenkins_client.make_request.side_effect = JenkinsError(
        "Connection failed"
    )

    with pytest.raises(JenkinsError, match="Connection failed"):
        common_service.get_jenkins_info()


def test_get_jenkins_info_unexpected_error(common_service):
    common_service.jenkins_client.make_request.side_effect = Exception(
        "Unexpected error"
    )

    with pytest.raises(Exception, match="Unexpected error"):
        common_service.get_jenkins_info()


def test_get_crumb_success(common_service):
    expected_response = {"crumb": "abcdef1234567890"}
    common_service.jenkins_client.make_request.return_value = expected_response

    result = common_service.get_crumb()

    assert result == expected_response
    common_service.jenkins_client.make_request.assert_called_once_with(
        CommonEndpoints.CRUMB_ISSUER, method="GET"
    )


def test_get_crumb_jenkins_error(common_service):
    common_service.jenkins_client.make_request.side_effect = JenkinsError(
        "CSRF protection disabled"
    )

    with pytest.raises(JenkinsError, match="CSRF protection disabled"):
        common_service.get_crumb()


def test_get_crumb_unexpected_error(common_service):
    common_service.jenkins_client.make_request.side_effect = Exception(
        "Unexpected error"
    )

    with pytest.raises(Exception, match="Unexpected error"):
        common_service.get_crumb()


def test_who_am_i_success(common_service):
    expected_response = {"id": "user123", "fullName": "John Doe"}
    common_service.jenkins_client.make_request.return_value = expected_response

    result = common_service.who_am_i()

    assert result == expected_response
    common_service.jenkins_client.make_request.assert_called_once_with(
        CommonEndpoints.WHOAMI_URL, method="GET", depth=1
    )


def test_who_am_i_custom_depth(common_service):
    expected_response = {
        "id": "user123",
        "fullName": "John Doe",
        "permissions": ["read", "write"],
    }
    common_service.jenkins_client.make_request.return_value = expected_response

    result = common_service.who_am_i(depth=2)

    assert result == expected_response
    common_service.jenkins_client.make_request.assert_called_once_with(
        CommonEndpoints.WHOAMI_URL, method="GET", depth=2
    )


def test_who_am_i_jenkins_error(common_service):
    common_service.jenkins_client.make_request.side_effect = JenkinsError(
        "Authentication failed"
    )

    with pytest.raises(JenkinsError, match="Authentication failed"):
        common_service.who_am_i()


def test_who_am_i_unexpected_error(common_service):
    common_service.jenkins_client.make_request.side_effect = Exception(
        "Unexpected error"
    )

    with pytest.raises(Exception, match="Unexpected error"):
        common_service.who_am_i()


@patch("deployit.providers.jenkins.services.common.RichPresenter")
def test_presenter_info_calls(mock_presenter, common_service):
    mock_presenter_instance = Mock()
    common_service.presenter = mock_presenter_instance
    common_service.jenkins_client.make_request.return_value = {}

    common_service.get_jenkins_info()
    common_service.get_crumb()
    common_service.who_am_i()

    assert (
        mock_presenter_instance.info.call_count == 6
    )  # 2 calls per method (start and success)


@patch("deployit.providers.jenkins.services.common.RichPresenter")
def test_presenter_error_calls(mock_presenter, common_service):
    mock_presenter_instance = Mock()
    common_service.presenter = mock_presenter_instance
    common_service.jenkins_client.make_request.side_effect = JenkinsError("Test error")

    with pytest.raises(JenkinsError):
        common_service.get_jenkins_info()
    with pytest.raises(JenkinsError):
        common_service.get_crumb()
    with pytest.raises(JenkinsError):
        common_service.who_am_i()

    assert mock_presenter_instance.error.call_count == 3  # 1 call per method
