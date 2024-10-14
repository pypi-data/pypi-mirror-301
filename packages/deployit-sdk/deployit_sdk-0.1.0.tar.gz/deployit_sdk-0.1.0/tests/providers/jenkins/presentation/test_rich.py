from unittest.mock import MagicMock, Mock, patch

import pytest
from rich.live import Live
from rich.table import Table

from deployit.providers.jenkins.models.base import JenkinsObject
from deployit.providers.jenkins.presentation.config import PresentationConfig
from deployit.providers.jenkins.presentation.rich import RichPresenter


@pytest.fixture(autouse=True)
def reset_singleton():
    RichPresenter._instance = None
    yield


@pytest.fixture
def mock_config():
    config = Mock(spec=PresentationConfig)
    config.use_rich_presentation = True
    config.logger = Mock()
    config.console = Mock()
    config.log = Mock()
    return config


@pytest.fixture
def rich_presenter(mock_config):
    return RichPresenter(mock_config)


@pytest.fixture
def mock_jenkins_objects():
    class MockJenkinsObject(JenkinsObject):
        def __init__(self, name, value):
            self.name = name
            self.value = value

        def to_dict(self):
            return {"name": self.name, "value": self.value}

    return [MockJenkinsObject("obj1", 1), MockJenkinsObject("obj2", 2)]


def test_display_jenkins_objects_empty(rich_presenter):
    with patch.object(rich_presenter, "display_error") as mock_display_error:
        rich_presenter.display_jenkins_objects("Test Objects", [])
        mock_display_error.assert_called_once_with("No objects to display.")


def test_display_dynamic_table_empty(rich_presenter):
    with patch.object(rich_presenter, "display_error") as mock_display_error:
        rich_presenter.display_dynamic_table("Test Dynamic Table", [])
        mock_display_error.assert_called_once_with("No items to display.")
