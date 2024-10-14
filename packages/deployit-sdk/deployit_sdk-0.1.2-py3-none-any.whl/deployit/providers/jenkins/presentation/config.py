import logging
import os

from rich.console import Console
from rich.logging import RichHandler


class PresentationConfig:
    """
    Configuration class for managing presentation and logging settings.

    Attributes
    ----------
    use_rich_presentation : bool
        Indicates whether to use rich presentation for console output.
    use_simple_logging : bool
        Indicates whether to use simple logging.
    use_rich_logging : bool
        Indicates whether to use rich logging with rich handler.
    logger : logging.Logger or None
        Logger instance configured based on the logging settings.

    Methods
    -------
    log(message: str) -> None
        Logs a message using the configured logger and optionally prints it to the console.
    """

    def __init__(self):
        """
        Initializes the PresentationConfig with settings from environment variables.

        Environment Variables
        ---------------------
        USE_RICH_PRESENTATION : str
            If set to 'true', '1', or 't', enables rich presentation.
        USE_SIMPLE_LOGGING : str
            If set to 'true', '1', or 't', enables simple logging.
        USE_RICH_LOGGING : str
            If set to 'true', '1', or 't', enables rich logging with rich handler.
        """
        self.use_rich_presentation = os.getenv(
            "USE_RICH_PRESENTATION", "False"
        ).lower() in ("true", "1", "t")
        self.use_simple_logging = os.getenv("USE_SIMPLE_LOGGING", "False").lower() in (
            "true",
            "1",
            "t",
        )
        self.use_rich_logging = os.getenv("USE_RICH_LOGGING", "False").lower() in (
            "true",
            "1",
            "t",
        )
        self.console = Console()
        if self.use_simple_logging:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger("job")
        elif self.use_rich_logging:
            logging.basicConfig(
                level="NOTSET",
                handlers=[RichHandler(rich_tracebacks=True, level="INFO")],
            )
            self.logger = logging.getLogger("job")
        else:
            self.logger = None

    def log(self, message: str) -> None:
        """
        Logs a message using the configured logger and optionally prints it to the console.

        Parameters
        ----------
        message : str
            The message to be logged and/or printed.
        """
        if self.logger:
            self.logger.info(message, extra={"markup": True})
