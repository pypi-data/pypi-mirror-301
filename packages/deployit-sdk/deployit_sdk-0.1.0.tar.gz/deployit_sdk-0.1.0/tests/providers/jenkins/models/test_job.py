import pytest

from deployit.providers.jenkins.models.base import JenkinsObject
from deployit.providers.jenkins.models.job import Job


@pytest.fixture
def sample_job_info():
    return {
        "fullName": "MyProject/MyJob",
        "name": "MyJob",
        "url": "http://jenkins.example.com/job/MyProject/job/MyJob/",
        "nextBuildNumber": 42,
        "concurrentBuild": True,
        "inQueue": False,
        "queueItem": None,
        "resumeBlocked": False,
        "buildable": True,
        "property": [
            {
                "_class": "hudson.model.ParametersDefinitionProperty",
                "parameterDefinitions": [
                    {
                        "name": "CHOICE_PARAM",
                        "description": "A choice parameter",
                        "_class": "hudson.model.ChoiceParameterDefinition",
                        "choices": ["option1", "option2", "option3"],
                    },
                    {
                        "name": "TEXT_PARAM",
                        "description": "A text parameter",
                        "_class": "hudson.model.TextParameterDefinition",
                    },
                    {
                        "name": "GIT_PARAM",
                        "description": "A git parameter",
                        "_class": "hudson.plugins.git.GitParameterDefinition",
                        "allValueItems": {"values": ["branch1", "branch2"]},
                    },
                ],
            }
        ],
        "jobs": [
            {
                "name": "SubJob1",
                "url": "http://jenkins.example.com/job/MyProject/job/MyJob/job/SubJob1/",
            },
            {
                "name": "SubJob2",
                "url": "http://jenkins.example.com/job/MyProject/job/MyJob/job/SubJob2/",
                "jobs": [
                    {
                        "name": "NestedJob",
                        "url": "http://jenkins.example.com/job/MyProject/job/MyJob/job/SubJob2/job/NestedJob/",
                    }
                ],
            },
        ],
    }


def test_job_initialization(sample_job_info):
    job = Job(sample_job_info)

    assert job.full_name == "MyProject/MyJob"
    assert job.name == "MyJob"
    assert job.url == "http://jenkins.example.com/job/MyProject/job/MyJob/"
    assert job.url_path == "/MyProject/MyJob/"
    assert job.next_build_number == 42
    assert job.concurrent_build == True
    assert job.in_queue == False
    assert job.queue_item == None
    assert job.resume_blocked == False
    assert job.buildable == True


def test_job_required_parameters(sample_job_info):
    job = Job(sample_job_info)

    assert len(job.required_parameters) == 3

    choice_param = next(
        param for param in job.required_parameters if param["name"] == "CHOICE_PARAM"
    )
    assert choice_param["description"] == "A choice parameter"
    assert choice_param["choices"] == ["option1", "option2", "option3"]

    text_param = next(
        param for param in job.required_parameters if param["name"] == "TEXT_PARAM"
    )
    assert text_param["description"] == "A text parameter"
    assert "choices" not in text_param

    git_param = next(
        param for param in job.required_parameters if param["name"] == "GIT_PARAM"
    )
    assert git_param["description"] == "A git parameter"
    assert git_param["values"] == ["branch1", "branch2"]


def test_job_subjobs(sample_job_info):
    job = Job(sample_job_info)

    assert len(job.subjobs) == 2
    assert isinstance(job.subjobs[0], Job)
    assert isinstance(job.subjobs[1], Job)

    assert job.subjobs[0].name == "SubJob1"
    assert job.subjobs[1].name == "SubJob2"

    assert len(job.subjobs[1].subjobs) == 1
    assert job.subjobs[1].subjobs[0].name == "NestedJob"


def test_job_update():
    job = Job({})  # Initialize with empty dict

    new_info = {
        "fullName": "UpdatedJob",
        "name": "UpdatedJob",
        "url": "http://jenkins.example.com/job/UpdatedJob/",
        "nextBuildNumber": 10,
        "concurrentBuild": False,
        "inQueue": True,
        "queueItem": {"id": 123},
        "resumeBlocked": True,
        "buildable": False,
    }

    job.update(new_info)

    assert job.full_name == "UpdatedJob"
    assert job.name == "UpdatedJob"
    assert job.url == "http://jenkins.example.com/job/UpdatedJob/"
    assert job.url_path == "/UpdatedJob/"
    assert job.next_build_number == 10
    assert job.concurrent_build == False
    assert job.in_queue == True
    assert job.queue_item == {"id": 123}
    assert job.resume_blocked == True
    assert job.buildable == False


def test_job_string_representation(sample_job_info):
    job = Job(sample_job_info)
    job_str = str(job)

    assert "full_name" in job_str
    assert "name" in job_str
    assert "url" in job_str
    assert "url_path" in job_str
    assert "next_build_number" in job_str
    assert "concurrent_build" in job_str
    assert "in_queue" in job_str
    assert "queue_item" in job_str
    assert "resume_blocked" in job_str
    assert "buildable" in job_str
    assert "required_parameters" in job_str
    assert "subjobs" in job_str


def test_job_to_dict(sample_job_info):
    job = Job(sample_job_info)
    job_dict = job.to_dict()

    assert job_dict["full_name"] == "MyProject/MyJob"
    assert job_dict["name"] == "MyJob"
    assert job_dict["url"] == "http://jenkins.example.com/job/MyProject/job/MyJob/"
    assert job_dict["url_path"] == "/MyProject/MyJob/"
    assert job_dict["next_build_number"] == 42
    assert job_dict["concurrent_build"] == True
    assert job_dict["in_queue"] == False
    assert job_dict["queue_item"] == None
    assert job_dict["resume_blocked"] == False
    assert job_dict["buildable"] == True
    assert len(job_dict["required_parameters"]) == 3
    assert len(job_dict["subjobs"]) == 2


def test_job_with_missing_values():
    incomplete_info = {"name": "IncompleteJob"}
    job = Job(incomplete_info)

    assert job.name == "IncompleteJob"
    assert job.full_name == None
    assert job.url == None
    assert job.url_path == "/"
    assert job.next_build_number == None
    assert job.concurrent_build == None
    assert job.in_queue == None
    assert job.queue_item == None
    assert job.resume_blocked == None
    assert job.buildable == None
    assert job.required_parameters == []
    assert job.subjobs == []


def test_job_inheritance():
    assert issubclass(Job, JenkinsObject)
