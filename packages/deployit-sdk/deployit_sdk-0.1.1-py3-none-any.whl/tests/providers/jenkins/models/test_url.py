from io import StringIO
from unittest.mock import MagicMock, Mock, patch

import pytest
from rich.console import Console

from deployit.providers.jenkins.models.url import JenkinsCrumb, JenkinsURLBuilder
from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.utils.config import Config


class SpyPresenter(RichPresenter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = kwargs.get("presentation_config", {}).get("console").file
        self.debug = MagicMock(wraps=self.debug)
        self.info = MagicMock(wraps=self.info)
        self.warn = MagicMock(wraps=self.warn)
        self.error = MagicMock(wraps=self.error)
        if isinstance(self.config, dict):

            class Config:
                pass

            config = Config()
            config.logger = self.config.get("logger")
            self.config = config

    def _debug(self, message):
        self.output.write(f"DEBUG: {message}\n")
        self.output.flush()  # Ensure the content is written immediately

    def _info(self, message):
        self.output.write(f"INFO: {message}\n")
        self.output.flush()  # Ensure the content is written immediately

    def _warn(self, message):
        self.output.write(f"WARN: {message}\n")
        self.output.flush()  # Ensure the content is written immediately

    def _error(self, message):
        self.output.write(f"ERROR: {message}\n")
        self.output.flush()  # Ensure the content is written immediately


@pytest.fixture
def captured_output():
    return StringIO()


@pytest.fixture
def mock_presenter(captured_output):
    console = Console(file=captured_output, force_terminal=True)
    return SpyPresenter(presentation_config={"console": console, "logger": Mock()})


@pytest.fixture
def url_builder(mock_presenter):
    return JenkinsURLBuilder(
        base_url="http://jenkins.example.com", presenter=mock_presenter
    )


def test_jenkins_crumb_initialization():
    crumb = JenkinsCrumb("test_crumb")
    assert crumb.crumb == "test_crumb"


def test_jenkins_url_builder_initialization():
    url_builder = JenkinsURLBuilder()
    assert url_builder.base_url == Config.JENKINS_DOMAIN
    assert isinstance(url_builder.presenter, RichPresenter)


def test_jenkins_url_builder_custom_initialization(mock_presenter):
    custom_base_url = "http://custom.jenkins.com"
    url_builder = JenkinsURLBuilder(base_url=custom_base_url, presenter=mock_presenter)
    assert url_builder.base_url == custom_base_url
    assert url_builder.presenter == mock_presenter


def test_build_url_simple(url_builder):
    endpoint_template = "/job/{job_name}/api/json"
    result = url_builder.build_url(endpoint_template, job_name="test-job")
    assert result == "http://jenkins.example.com/job/test-job/api/json"


def test_build_url_with_base_url(url_builder):
    endpoint_template = "{base_url}/api/json"
    result = url_builder.build_url(
        endpoint_template, base_url="/folder1/folder2/job-name"
    )
    assert (
        result
        == "http://jenkins.example.com/job/folder1/job/folder2/job/job-name/api/json"
    )


def test_build_url_with_query(url_builder):
    endpoint_template = "/job/{job_name}/api/json"
    result = url_builder.build_url(
        endpoint_template, job_name="test-job", query="depth=1"
    )
    assert result == "http://jenkins.example.com/job/test-job/api/json?depth=1"


def test_build_url_with_short_query(url_builder):
    endpoint_template = "/job/{job_name}/api/json"
    result = url_builder.build_url(endpoint_template, job_name="test-job", query="a=1")
    assert result == "http://jenkins.example.com/job/test-job/api/json?a=1"


def test_build_url_missing_parameter(url_builder):
    endpoint_template = "/job/{job_name}/api/json"
    with pytest.raises(KeyError):
        url_builder.build_url(endpoint_template)


def test_build_url_general_exception(url_builder):
    endpoint_template = "/job/{job_name}/api/json"
    result = url_builder.build_url(endpoint_template, job_name=object())
    assert "object" in result  # or any other appropriate assertion


def test_jenkins_url_builder_default_initialization():
    url_builder = JenkinsURLBuilder()
    assert url_builder.base_url == "localhost"


def test_build_url_with_existing_job_path(url_builder):
    endpoint_template = "{base_url}/api/json"
    result = url_builder.build_url(
        endpoint_template, base_url="/folder1/folder2/job-name"
    )
    assert (
        result
        == "http://jenkins.example.com/job/folder1/job/folder2/job/job-name/api/json"
    )


def test_build_url_attribute_after_successful_build(url_builder):
    endpoint_template = "/job/{job_name}/api/json"
    url_builder.build_url(endpoint_template, job_name="test-job")
    assert hasattr(url_builder, "complete_url")
    assert (
        url_builder.complete_url == "http://jenkins.example.com/job/test-job/api/json"
    )
