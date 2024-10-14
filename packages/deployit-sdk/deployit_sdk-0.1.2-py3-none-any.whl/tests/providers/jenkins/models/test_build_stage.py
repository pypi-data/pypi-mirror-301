from unittest.mock import patch

import pytest

from deployit.providers.jenkins.models.base import JenkinsObject
from deployit.providers.jenkins.models.build_stage import JenkinsBuildStage


@pytest.fixture
def sample_stage_info():
    return {
        "id": "1",
        "buildId": "100",
        "name": "Build",
        "status": "SUCCESS",
        "startTimeMillis": 1631234567890,
        "durationMillis": 120000,
        "pauseDurationMillis": 30000,
    }


@patch("deployit.providers.jenkins.models.build_stage.convert_timestamp")
@patch("deployit.providers.jenkins.models.build_stage.convert_duration")
def test_jenkins_build_stage_initialization(
    mock_convert_duration, mock_convert_timestamp, sample_stage_info
):
    mock_convert_timestamp.return_value = "2021-09-10 12:34:56"
    mock_convert_duration.side_effect = ["2m 0s", "0m 30s"]

    stage = JenkinsBuildStage(sample_stage_info)

    assert stage.id == "1"
    assert stage.build_id == "100"
    assert stage.name == "Build"
    assert stage.status == "SUCCESS"
    assert stage.start_time == "2021-09-10 12:34:56"
    assert stage.duration == "2m 0s"
    assert stage.pause_duration == "0m 30s"

    mock_convert_timestamp.assert_called_once_with(1631234567890)
    mock_convert_duration.assert_any_call(120000)
    mock_convert_duration.assert_any_call(30000)


def test_jenkins_build_stage_string_representation(sample_stage_info):
    stage = JenkinsBuildStage(sample_stage_info)
    stage_str = str(stage)

    assert "id" in stage_str
    assert "build_id" in stage_str
    assert "name" in stage_str
    assert "status" in stage_str
    assert "start_time" in stage_str
    assert "duration" in stage_str
    assert "pause_duration" in stage_str


def test_jenkins_build_stage_to_dict(sample_stage_info):
    stage = JenkinsBuildStage(sample_stage_info)
    stage_dict = stage.to_dict()

    assert stage_dict["id"] == "1"
    assert stage_dict["build_id"] == "100"
    assert stage_dict["name"] == "Build"
    assert stage_dict["status"] == "SUCCESS"
    assert "start_time" in stage_dict
    assert "duration" in stage_dict
    assert "pause_duration" in stage_dict


@patch("deployit.providers.jenkins.models.build_stage.convert_timestamp")
@patch("deployit.providers.jenkins.models.build_stage.convert_duration")
def test_jenkins_build_stage_with_missing_values(
    mock_convert_duration, mock_convert_timestamp
):
    incomplete_info = {"id": "1", "name": "Build"}

    mock_convert_timestamp.return_value = None
    mock_convert_duration.return_value = None

    stage = JenkinsBuildStage(incomplete_info)

    assert stage.id == "1"
    assert stage.name == "Build"
    assert stage.build_id is None
    assert stage.status is None
    assert stage.start_time is None
    assert stage.duration is None
    assert stage.pause_duration is None

    mock_convert_timestamp.assert_called_once_with(0)
    assert mock_convert_duration.call_count == 2


@patch("deployit.providers.jenkins.models.build_stage.convert_timestamp")
@patch("deployit.providers.jenkins.models.build_stage.convert_duration")
def test_jenkins_build_stage_with_none_values(
    mock_convert_duration, mock_convert_timestamp, sample_stage_info
):
    for key in sample_stage_info:
        sample_stage_info[key] = None

    mock_convert_timestamp.return_value = None
    mock_convert_duration.return_value = None

    stage = JenkinsBuildStage(sample_stage_info)

    assert stage.id is None
    assert stage.build_id is None
    assert stage.name is None
    assert stage.status is None
    assert stage.start_time is None
    assert stage.duration is None
    assert stage.pause_duration is None

    mock_convert_timestamp.assert_called_once_with(0)
    assert mock_convert_duration.call_count == 2


def test_jenkins_build_stage_inheritance():
    assert issubclass(JenkinsBuildStage, JenkinsObject)
