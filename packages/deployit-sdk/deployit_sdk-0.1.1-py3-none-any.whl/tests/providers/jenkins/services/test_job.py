from unittest.mock import Mock, patch

import pytest

from deployit.providers.jenkins.endpoints.job import JobEndpoints
from deployit.providers.jenkins.models.build import Build
from deployit.providers.jenkins.models.job import Job
from deployit.providers.jenkins.services.job import JenkinsJobApiService
from deployit.providers.jenkins.utils.errors import JenkinsAPIError


@pytest.fixture
def mock_jenkins_client():
    return Mock()


@pytest.fixture
def mock_build_service():
    return Mock()


@pytest.fixture
def job_service(mock_jenkins_client, mock_build_service):
    return JenkinsJobApiService(mock_jenkins_client, mock_build_service)


def test_get_all(job_service, mock_jenkins_client):
    mock_jenkins_client.make_request.return_value = {
        "jobs": [{"name": "job1"}, {"name": "job2"}]
    }
    result = job_service.get_all("jobs[name]")
    assert result == {"jobs": [{"name": "job1"}, {"name": "job2"}]}
    mock_jenkins_client.make_request.assert_called_once_with(
        JobEndpoints.JOBS_QUERY, method="GET", tree="jobs[name]"
    )


def test_get_info(job_service, mock_jenkins_client):
    mock_jenkins_client.make_request.return_value = {
        "name": "test_job",
        "url": "http://jenkins.example.com/job/test_job",
    }
    result = job_service.get_info("/job/test_job")
    assert isinstance(result, Job)
    assert result.name == "test_job"
    mock_jenkins_client.make_request.assert_called_once_with(
        JobEndpoints.JOB_INFO, method="GET", base_url="/job/test_job", depth=1
    )


@patch("time.time", side_effect=[0, 60, 120])
@patch("time.sleep", return_value=None)
def test_wait_for_build_success(mock_sleep, mock_time, job_service, mock_build_service):
    build = Build({"queueId": 123})
    mock_build_service.refresh_build.side_effect = [
        Build({"queueId": 123}),
        Build({"queueId": 123, "number": 1}),
    ]
    result = job_service.wait_for_build(build, timeout=180)
    assert result.number == 1
    assert mock_build_service.refresh_build.call_count == 2


@patch("time.time", side_effect=[0, 60, 120, 180])
@patch("time.sleep", return_value=None)
def test_wait_for_build_timeout(mock_sleep, mock_time, job_service, mock_build_service):
    build = Build({"queueId": 123})
    mock_build_service.refresh_build.return_value = Build({"queueId": 123})
    with pytest.raises(TimeoutError):
        job_service.wait_for_build(build)


def test_build(job_service, mock_jenkins_client):
    mock_jenkins_client.make_request.return_value = {
        "Location": "http://jenkins.example.com/queue/item/123/"
    }
    result = job_service.build("/job/test_job")
    assert isinstance(result, Build)
    assert result.queue_id == 123
    mock_jenkins_client.make_request.assert_called_once_with(
        JobEndpoints.BUILD_JOB, method="POST", base_url="/job/test_job"
    )


def test_build_with_params(job_service, mock_jenkins_client):
    mock_jenkins_client.make_request.return_value = {"success": True}
    result = job_service.build("/job/test_job", {"param1": "value1"})
    assert isinstance(result, Build)
    mock_jenkins_client.make_request.assert_called_once_with(
        JobEndpoints.BUILD_WITH_PARAMETERS,
        method="POST",
        query="name=param1&value=value1",
        base_url="/job/test_job",
    )


def test_get_all_builds(job_service, mock_jenkins_client):
    mock_jenkins_client.make_request.return_value = {
        "allBuilds": [{"number": 1}, {"number": 2}]
    }
    result = job_service.get_all_builds("/job/test_job")
    assert result == {"allBuilds": [{"number": 1}, {"number": 2}]}
    mock_jenkins_client.make_request.assert_called_once_with(
        JobEndpoints.ALL_BUILDS, method="GET", base_url="/job/test_job"
    )


def test_fetch_job_details(job_service):
    job = Job(
        {
            "name": "test_job",
            "url": "http://jenkins.example.com/job/test_job",
            "fullName": "/job/test_job",
        }
    )
    with patch.object(
        job_service,
        "get_info",
        return_value=Job(
            {
                "name": "test_job",
                "url": "http://jenkins.example.com/job/test_job",
            }
        ),
    ):
        with patch.object(job_service, "fetch_builds", return_value=[]):
            result = job_service.fetch_job_details(job)
    assert isinstance(result, Job)
    assert result.name == "test_job"
    assert result.build_history == []


def test_fetch_builds(job_service):
    job = Job(
        {
            "name": "test_job",
            "url": "http://jenkins.example.com/job/test_job",
            "urlPath": "/job/test_job",
        }
    )
    with patch.object(
        job_service,
        "get_all_builds",
        return_value={"allBuilds": [{"number": 1}, {"number": 2}]},
    ):
        result = job_service.fetch_builds(job)
    assert len(result) == 2
    assert all(isinstance(build, Build) for build in result)


def test_fetch_builds_with_filter(job_service):
    job = Job(
        {
            "name": "test_job",
            "url": "http://jenkins.example.com/job/test_job",
            "urlPath": "/job/test_job",
        }
    )
    with patch.object(
        job_service,
        "get_all_builds",
        return_value={
            "allBuilds": [
                {"number": 1, "result": "SUCCESS"},
                {"number": 2, "result": "FAILURE"},
            ]
        },
    ):
        result = job_service.fetch_builds(job, filter_by={"result": "SUCCESS"})
    assert len(result) == 1
    assert result[0].number == 1


def test_error_handling(job_service, mock_jenkins_client):
    mock_jenkins_client.make_request.side_effect = Exception("API Error")
    with pytest.raises(Exception):
        job_service.get_all("jobs[name]")
