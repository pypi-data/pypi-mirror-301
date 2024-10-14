from unittest.mock import Mock, patch

import pytest

from deployit.providers.jenkins.models.build_stage import JenkinsBuildStage
from deployit.providers.jenkins.services.build_stage import JenkinsBuildStageService
from deployit.providers.jenkins.utils.errors import JenkinsError


@pytest.fixture
def mock_jenkins_client():
    return Mock()


@pytest.fixture
def build_stage_service(mock_jenkins_client):
    return JenkinsBuildStageService(mock_jenkins_client)


@pytest.fixture
def sample_build_stage():
    return JenkinsBuildStage(
        {
            "id": "1",
            "buildId": "100",
            "name": "Input Stage",
            "status": "PAUSED_PENDING_INPUT",
        }
    )


def test_handle_input_abort(build_stage_service, sample_build_stage):
    build_stage_service.jenkins_client.make_request.return_value = Mock(
        json=lambda: {"status": "aborted"}
    )

    result = build_stage_service.handle_input("/test", sample_build_stage, "abort")

    assert result == {"status": "aborted"}
    build_stage_service.jenkins_client.make_request.assert_called_once_with(
        "/job/test/100/input/1/abort", method="POST", data=None
    )


def test_handle_input_proceed_empty(build_stage_service, sample_build_stage):
    build_stage_service.jenkins_client.make_request.return_value = Mock(
        json=lambda: {"status": "proceeded"}
    )

    result = build_stage_service.handle_input(
        "/test", sample_build_stage, "proceedEmpty"
    )

    assert result == {"status": "proceeded"}
    build_stage_service.jenkins_client.make_request.assert_called_once_with(
        "/job/test/100/input/1/proceedEmpty", method="POST", data=None
    )


def test_handle_input_submit(build_stage_service, sample_build_stage):
    build_stage_service.jenkins_client.make_request.return_value = Mock(
        json=lambda: {"status": "submitted"}
    )

    result = build_stage_service.handle_input(
        "/test",
        sample_build_stage,
        "submit",
        proceed_caption="Proceed",
        parameters={"key": "value"},
    )

    assert result == {"status": "submitted"}
    build_stage_service.jenkins_client.make_request.assert_called_once_with(
        "/job/test/100/input/1/submit",
        method="POST",
        data={"proceed": "Proceed", "json": '{"parameter": {"key": "value"}}'},
    )


def test_handle_input_wfapi_input_submit(build_stage_service, sample_build_stage):
    build_stage_service.jenkins_client.make_request.return_value = Mock(
        json=lambda: {"status": "submitted"}
    )

    result = build_stage_service.handle_input(
        "/test",
        sample_build_stage,
        "wfapi/inputSubmit",
        proceed_caption="Proceed",
        parameters={"key": "value"},
    )

    assert result == {"status": "submitted"}
    build_stage_service.jenkins_client.make_request.assert_called_once_with(
        "/job/test/100/wfapi/inputSubmit?inputId=UserInput",
        method="POST",
        data="json=%7B%22parameter%22%3A%20%5B%7B%22name%22%3A%20%22key%22%2C%20%22value%22%3A%20%22value%22%7D%5D%7D",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
        },
        is_json=False,
    )


def test_handle_input_invalid_action(build_stage_service, sample_build_stage):
    with pytest.raises(ValueError, match="Invalid action specified"):
        build_stage_service.handle_input("/test", sample_build_stage, "invalid_action")


def test_handle_input_submit_without_proceed_caption(
    build_stage_service, sample_build_stage
):
    with pytest.raises(
        ValueError, match="'proceed_caption' is required for 'submit' action"
    ):
        build_stage_service.handle_input("/test", sample_build_stage, "submit")


def test_handle_input_jenkins_error(build_stage_service, sample_build_stage):
    build_stage_service.jenkins_client.make_request.side_effect = JenkinsError(
        "Jenkins error"
    )

    with pytest.raises(JenkinsError, match="Jenkins error"):
        build_stage_service.handle_input("/test", sample_build_stage, "abort")


def test_handle_input_unexpected_error(build_stage_service, sample_build_stage):
    build_stage_service.jenkins_client.make_request.side_effect = Exception(
        "Unexpected error"
    )

    with pytest.raises(Exception, match="Unexpected error"):
        build_stage_service.handle_input("/test", sample_build_stage, "abort")


def test_handle_input_with_nested_job_path(build_stage_service, sample_build_stage):
    build_stage_service.jenkins_client.make_request.return_value = Mock(
        json=lambda: {"status": "aborted"}
    )

    result = build_stage_service.handle_input(
        "/folder1/folder2/test", sample_build_stage, "abort"
    )

    assert result == {"status": "aborted"}
    build_stage_service.jenkins_client.make_request.assert_called_once_with(
        "/job/folder1/job/folder2/job/test/100/input/1/abort", method="POST", data=None
    )


def test_handle_input_without_parameters(build_stage_service, sample_build_stage):
    build_stage_service.jenkins_client.make_request.return_value = Mock(
        json=lambda: {"status": "submitted"}
    )

    result = build_stage_service.handle_input(
        "/test", sample_build_stage, "submit", proceed_caption="Proceed"
    )

    assert result == {"status": "submitted"}
    build_stage_service.jenkins_client.make_request.assert_called_once_with(
        "/job/test/100/input/1/submit",
        method="POST",
        data={"proceed": "Proceed", "json": ""},
    )


def test_handle_input_response_without_content(build_stage_service, sample_build_stage):
    build_stage_service.jenkins_client.make_request.return_value = {}

    result = build_stage_service.handle_input("/test", sample_build_stage, "abort")

    assert result == {}
