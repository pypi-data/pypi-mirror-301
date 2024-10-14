import logging
from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console
from rich.logging import RichHandler

from deployit.providers.jenkins.presentation.config import PresentationConfig


@pytest.fixture
def mock_env_vars():
    with patch.dict(
        "os.environ",
        {
            "USE_RICH_PRESENTATION": "false",
            "USE_SIMPLE_LOGGING": "false",
            "USE_RICH_LOGGING": "false",
        },
        clear=True,
    ):
        yield


def test_default_initialization(mock_env_vars):
    config = PresentationConfig()
    assert not config.use_rich_presentation
    assert not config.use_simple_logging
    assert not config.use_rich_logging
    assert isinstance(config.console, Console)
    assert config.logger is None


@pytest.mark.parametrize(
    "env_var, attr",
    [
        ("USE_RICH_PRESENTATION", "use_rich_presentation"),
        ("USE_SIMPLE_LOGGING", "use_simple_logging"),
        ("USE_RICH_LOGGING", "use_rich_logging"),
    ],
)
@pytest.mark.parametrize(
    "value, expected",
    [
        ("true", True),
        ("1", True),
        ("t", True),
        ("false", False),
        ("0", False),
        ("f", False),
    ],
)
def test_environment_variable_parsing(mock_env_vars, env_var, attr, value, expected):
    with patch.dict("os.environ", {env_var: value}):
        config = PresentationConfig()
        assert getattr(config, attr) == expected


@patch("logging.basicConfig")
@patch("logging.getLogger")
def test_simple_logging_configuration(
    mock_get_logger, mock_basic_config, mock_env_vars
):
    with patch.dict("os.environ", {"USE_SIMPLE_LOGGING": "true"}):
        config = PresentationConfig()
        mock_basic_config.assert_called_once_with(level=logging.INFO)
        mock_get_logger.assert_called_once_with("job")
        assert config.logger == mock_get_logger.return_value


@patch("logging.basicConfig")
@patch("logging.getLogger")
def test_rich_logging_configuration(mock_get_logger, mock_basic_config, mock_env_vars):
    with patch.dict("os.environ", {"USE_RICH_LOGGING": "true"}):
        config = PresentationConfig()
        mock_basic_config.assert_called_once()
        call_args = mock_basic_config.call_args[1]  # Get kwargs of the call
        assert call_args["level"] == "NOTSET"
        assert len(call_args["handlers"]) == 1
        handler = call_args["handlers"][0]
        assert isinstance(handler, RichHandler)
        assert handler.level == 20
        assert handler.rich_tracebacks is True
        mock_get_logger.assert_called_once_with("job")
        assert config.logger == mock_get_logger.return_value


def test_log_method_with_logger():
    config = PresentationConfig()
    config.logger = MagicMock()
    message = "Test message"
    config.log(message)
    config.logger.info.assert_called_once_with(message, extra={"markup": True})


def test_log_method_without_logger(capsys):
    config = PresentationConfig()
    config.logger = None
    message = "Test message"
    config.log(message)
    captured = capsys.readouterr()
    assert captured.out == ""  # No output when logger is None


@pytest.mark.parametrize("use_rich_presentation", [True, False])
def test_console_creation(mock_env_vars, use_rich_presentation):
    with patch.dict(
        "os.environ", {"USE_RICH_PRESENTATION": str(use_rich_presentation).lower()}
    ):
        config = PresentationConfig()
        assert isinstance(config.console, Console)


def test_multiple_instances_independence(mock_env_vars):
    with patch.dict("os.environ", {"USE_SIMPLE_LOGGING": "true"}):
        config1 = PresentationConfig()
    with patch.dict("os.environ", {"USE_RICH_LOGGING": "true"}):
        config2 = PresentationConfig()

    assert config1.use_simple_logging
    assert not config1.use_rich_logging
    assert not config2.use_simple_logging
    assert config2.use_rich_logging
