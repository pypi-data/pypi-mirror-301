from unittest.mock import MagicMock, patch

import pytest

from deployit.providers.jenkins.models.base import JenkinsObject
from deployit.providers.jenkins.models.build import Build


@pytest.fixture
def sample_build_info():
    return {
        "building": False,
        "description": "Test build",
        "duration": 120000,
        "estimatedDuration": 150000,
        "id": "123",
        "keepLog": True,
        "number": 42,
        "queueId": 1000,
        "result": "SUCCESS",
        "timestamp": 1631234567890,
        "inProgress": False,
        "url": "http://jenkins.example.com/job/test-job/42/",
        "actions": [
            {
                "_class": "hudson.plugins.sonar.action.SonarAnalysisAction",
                "sonarqubeDashboardUrl": "http://sonar.example.com/dashboard?id=test-project",
            },
            {
                "_class": "hudson.model.CauseAction",
                "causes": [
                    {
                        "_class": "hudson.model.Cause$UserIdCause",
                        "userId": "john.doe",
                        "userName": "John Doe",
                    }
                ],
            },
        ],
        "changeSets": [],
    }


@patch("deployit.providers.jenkins.models.build.convert_timestamp")
@patch("deployit.providers.jenkins.models.build.convert_duration")
def test_build_initialization(
    mock_convert_duration, mock_convert_timestamp, sample_build_info
):
    mock_convert_timestamp.return_value = "2021-09-10 12:34:56"
    mock_convert_duration.side_effect = ["2m 0s", "2m 30s"]

    build = Build(sample_build_info)

    assert build.sonar_link == "http://sonar.example.com/dashboard?id=test-project"
    assert build.cause == {"userId": "john.doe", "userName": "John Doe"}
    assert build.is_building == False
    assert build.description == "Test build"
    assert build.duration == "2m 0s"
    assert build.estimated_duration == "2m 30s"
    assert build.id == "123"
    assert build.keep_log == True
    assert build.number == 42
    assert build.queue_id == 1000
    assert build.result == "SUCCESS"
    assert build.timestamp == "2021-09-10 12:34:56"
    assert build.in_progress == False
    assert build.url == "http://jenkins.example.com/job/test-job/42/"
    assert build.url_path == "/test-job"

    mock_convert_timestamp.assert_called_once_with(1631234567890)
    mock_convert_duration.assert_any_call(120000)
    mock_convert_duration.assert_any_call(150000)


def test_build_update(sample_build_info):
    build = Build({})  # Initialize with empty dict
    build.update(sample_build_info)

    assert build.sonar_link == "http://sonar.example.com/dashboard?id=test-project"
    assert build.cause == {"userId": "john.doe", "userName": "John Doe"}
    assert build.is_building == False
    assert build.description == "Test build"
    assert build.id == "123"
    assert build.keep_log == True
    assert build.number == 42
    assert build.queue_id == 1000
    assert build.result == "SUCCESS"
    assert build.in_progress == False
    assert build.url == "http://jenkins.example.com/job/test-job/42/"
    assert build.url_path == "/test-job"


def test_build_get_sonar_link():
    build_info = {
        "actions": [
            {
                "_class": "hudson.plugins.sonar.action.SonarAnalysisAction",
                "sonarqubeDashboardUrl": "http://sonar.example.com/dashboard?id=test-project",
            }
        ]
    }
    build = Build(build_info)
    assert build.sonar_link == "http://sonar.example.com/dashboard?id=test-project"


def test_build_get_cause_user_id():
    build_info = {
        "actions": [
            {
                "_class": "hudson.model.CauseAction",
                "causes": [
                    {
                        "_class": "hudson.model.Cause$UserIdCause",
                        "userId": "john.doe",
                        "userName": "John Doe",
                    }
                ],
            }
        ]
    }
    build = Build(build_info)
    assert build.cause == {"userId": "john.doe", "userName": "John Doe"}


def test_build_get_cause_branch_event():
    build_info = {
        "actions": [
            {
                "_class": "hudson.model.CauseAction",
                "causes": [{"_class": "jenkins.branch.BranchEventCause"}],
            },
            {
                "_class": "hudson.plugins.git.util.BuildData",
                "remoteUrls": ["https://github.com/example/repo.git"],
            },
        ],
        "changeSets": [
            {
                "_class": "hudson.plugins.git.GitChangeSetList",
                "items": [
                    {
                        "commitId": "abcdef123456",
                        "author": {"fullName": "John Doe"},
                        "authorEmail": "john.doe@example.com",
                        "date": "2021-09-10 12:00:00",
                        "msg": "Test commit",
                        "affectedPaths": ["file1.txt", "file2.txt"],
                        "paths": [
                            {"file": "file1.txt", "editType": "edit"},
                            {"file": "file2.txt", "editType": "add"},
                        ],
                    }
                ],
            }
        ],
    }
    build = Build(build_info)
    expected_cause = {
        "remoteUrls": ["https://github.com/example/repo.git"],
        "affectedPaths": ["file1.txt", "file2.txt"],
        "commitId": "abcdef123456",
        "authorFullName": "John Doe",
        "authorEmail": "john.doe@example.com",
        "date": "2021-09-10 12:00:00",
        "msg": "Test commit",
        "editTypes": [
            {"file": "file1.txt", "editType": "edit"},
            {"file": "file2.txt", "editType": "add"},
        ],
    }
    assert build.cause == expected_cause


def test_build_string_representation(sample_build_info):
    build = Build(sample_build_info)
    build_str = str(build)

    assert "sonar_link" in build_str
    assert "cause" in build_str
    assert "is_building" in build_str
    assert "description" in build_str
    assert "duration" in build_str
    assert "estimated_duration" in build_str
    assert "id" in build_str
    assert "keep_log" in build_str
    assert "number" in build_str
    assert "queue_id" in build_str
    assert "result" in build_str
    assert "timestamp" in build_str
    assert "in_progress" in build_str
    assert "url" in build_str
    assert "url_path" in build_str


def test_build_to_dict(sample_build_info):
    build = Build(sample_build_info)
    build_dict = build.to_dict()

    assert (
        build_dict["sonar_link"] == "http://sonar.example.com/dashboard?id=test-project"
    )
    assert build_dict["cause"] == {"userId": "john.doe", "userName": "John Doe"}
    assert build_dict["is_building"] == False
    assert build_dict["description"] == "Test build"
    assert "duration" in build_dict
    assert "estimated_duration" in build_dict
    assert build_dict["id"] == "123"
    assert build_dict["keep_log"] == True
    assert build_dict["number"] == 42
    assert build_dict["queue_id"] == 1000
    assert build_dict["result"] == "SUCCESS"
    assert "timestamp" in build_dict
    assert build_dict["in_progress"] == False
    assert build_dict["url"] == "http://jenkins.example.com/job/test-job/42/"
    assert build_dict["url_path"] == "/test-job"


def test_build_with_missing_values():
    incomplete_info = {"id": "123", "number": 42}
    build = Build(incomplete_info)

    assert build.id == "123"
    assert build.number == 42
    assert build.sonar_link is None
    assert build.cause is None
    assert build.is_building == False
    assert build.description is None
    assert build.duration == "0m 0s"
    assert build.estimated_duration == "0m 0s"
    assert build.keep_log == False
    assert build.queue_id is None
    assert build.result is None
    assert build.in_progress == False
    assert build.url is None
    assert build.url_path == "/"


def test_build_inheritance():
    assert issubclass(Build, JenkinsObject)
