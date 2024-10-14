from unittest.mock import MagicMock, Mock, patch

import pytest

from deployit.providers.jenkins.models.build import Build
from deployit.providers.jenkins.models.build_stage import JenkinsBuildStage
from deployit.providers.jenkins.services.build import JenkinsBuildApiService
from deployit.providers.jenkins.utils.errors import JenkinsError


@pytest.fixture
def mock_jenkins_client():
    return Mock()


@pytest.fixture
def mock_queue_service():
    return Mock()


@pytest.fixture
def build_service(mock_jenkins_client, mock_queue_service):
    return JenkinsBuildApiService(mock_jenkins_client, mock_queue_service)


def test_refresh_build_queued(build_service):
    build = Build(
        {"queueId": "123", "url": "/job/test"}
    )  # Change 'queue_id' to 'queueId' and 'url_path' to 'url'
    mock_queue_item = Mock(buildable=True, build_id=456)
    build_service.queue_service.get_queue_item.return_value = mock_queue_item
    build_service.jenkins_client.make_request.return_value = {"number": 456}

    refreshed_build = build_service.refresh_build(build)

    assert refreshed_build.number == 456


def test_refresh_build_not_queued(build_service):
    build = Build({"url_path": "/job/test"})

    with pytest.raises(ValueError, match="Build is not queued, cannot refresh."):
        build_service.refresh_build(build)


def test_extract_job_info():
    url = "http://jenkins.example.com/job/folder1/job/folder2/job/test-job/"
    folder_url, short_name = JenkinsBuildApiService.extract_job_info(url)

    assert folder_url == "http://jenkins.example.com/job/folder1/job/folder2/job/"
    assert short_name == "test-job"


def test_stop_build(build_service):
    build_service.jenkins_client.make_request.return_value = {"status": "stopped"}

    response = build_service.stop("/job/test", 123)

    assert response == {"status": "stopped"}
    build_service.jenkins_client.make_request.assert_called_once()


def test_stop_build_error(build_service):
    build_service.jenkins_client.make_request.side_effect = JenkinsError("Test error")

    with pytest.raises(JenkinsError, match="Test error"):
        build_service.stop("/job/test", 123)


def test_get_build_info(build_service):
    build_service.jenkins_client.make_request.return_value = {"number": 123}
    build_service.get_stages = Mock(return_value=[])

    build = build_service.get_build_info("/job/test", 123)

    assert isinstance(build, Build)
    assert build.number == 123
    build_service.jenkins_client.make_request.assert_called_once()
    build_service.get_stages.assert_called_once()


def test_get_console_log(build_service):
    build_service.jenkins_client.make_request.return_value = {"content": "Test output"}

    output = build_service.get_console_log("/job/test", 123)

    assert output == {"content": "Test output"}
    build_service.jenkins_client.make_request.assert_called_once()


def test_get_env_vars(build_service):
    build_service.jenkins_client.make_request.return_value = {"VAR1": "value1"}

    env_vars = build_service.get_env_vars("/job/test", 123)

    assert env_vars == {"VAR1": "value1"}
    build_service.jenkins_client.make_request.assert_called_once()


def test_get_test_report(build_service):
    build_service.jenkins_client.make_request.return_value = {"tests": []}

    report = build_service.get_test_report("/job/test", 123)

    assert report == {"tests": []}
    build_service.jenkins_client.make_request.assert_called_once()


def test_get_artifact(build_service):
    build_service.jenkins_client.make_request.return_value = {"artifact": "data"}

    artifact = build_service.get_artifact("/job/test", 123, "artifact.txt")

    assert artifact == {"artifact": "data"}
    build_service.jenkins_client.make_request.assert_called_once()


def test_get_pending_stages(build_service):
    build_service.get_stages = Mock(
        return_value=[
            JenkinsBuildStage(
                {
                    "id": "1",
                    "status": "PAUSED_PENDING_INPUT",
                    "startTimeMillis": 1631234567890,
                    "durationMillis": 1000,
                    "pauseDurationMillis": 500,
                }
            ),
            JenkinsBuildStage(
                {
                    "id": "2",
                    "status": "SUCCESS",
                    "startTimeMillis": 1631234567890,
                    "durationMillis": 2000,
                    "pauseDurationMillis": 0,
                }
            ),
        ]
    )

    pending_stages = build_service.get_pending_stages("/job/test", 123)

    assert len(pending_stages) == 1
    assert pending_stages[0].id == "1"


def test_get_stages(build_service):
    build_service.jenkins_client.make_request.return_value = {
        "stages": [
            {
                "id": "1",
                "startTimeMillis": 1631234567890,
                "durationMillis": 1000,
                "pauseDurationMillis": 500,
            },
            {
                "id": "2",
                "startTimeMillis": 1631234567890,
                "durationMillis": 2000,
                "pauseDurationMillis": 0,
            },
        ]
    }

    stages = build_service.get_stages("/job/test", 123)

    assert len(stages) == 2
    assert all(isinstance(stage, JenkinsBuildStage) for stage in stages)


def test_get_stages(build_service):
    build_service.jenkins_client.make_request.return_value = {
        "stages": [
            {"id": "1", "startTimeMillis": 1631234567890, "durationMillis": 1000},
            {"id": "2", "startTimeMillis": 1631234567890, "durationMillis": 2000},
        ]
    }

    stages = build_service.get_stages("/job/test", 123)

    assert len(stages) == 2
    assert all(isinstance(stage, JenkinsBuildStage) for stage in stages)


def test_fetch_status(build_service):
    build = Build({"number": 123})
    build_service.get_build_info = Mock(
        return_value=Build({"number": 123, "result": "SUCCESS"})
    )

    status = build_service.fetch_status(build, "/job/test")

    assert status == "SUCCESS"


def test_fetch_status_error(build_service):
    build = Build({"number": 123})
    build_service.get_build_info = Mock(side_effect=JenkinsError("Test error"))

    with pytest.raises(JenkinsError, match="Test error"):
        build_service.fetch_status(build, "/job/test")
