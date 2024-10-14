from typing import Any, List, Optional

from rich.live import Live
from rich.table import Table

from deployit.providers.jenkins.presentation.config import PresentationConfig
from deployit.providers.jenkins.utils.decorators import make_singleton


@make_singleton
class RichPresenter:
    def __init__(self, presentation_config: Optional[PresentationConfig] = None):
        self.config = presentation_config or PresentationConfig()

    def print(self, message: Any) -> None:
        """
        Print a message to the console.

        Parameters
        ----------
        message : str
            The message to print.
        """
        if self.config.use_rich_presentation:
            self.config.console.print(message)
        if self.config.logger and not isinstance(message, Table):
            self.config.log(message)

    def display_jenkins_objects(
        self,
        title: str,
        objects: List[Any],
        include_columns: Optional[List[str]] = None,
    ) -> None:
        """
        Display a list of Jenkins objects.

        Parameters
        ----------
        title : str
            The title of the table.
        objects : List[Any]
            A list of Jenkins objects to display.
        include_columns : List[str], optional
            A list of columns to include in the table.
        """
        table = Table(title=title, show_header=True)
        object_dicts = [jenkins_obj.to_dict() for jenkins_obj in objects]
        if not object_dicts:
            self.display_error("No objects to display.")
            return

        first_object = object_dicts[0]
        columns = include_columns if include_columns else list(first_object.keys())

        for column in columns:
            table.add_column(column.capitalize(), justify="right")

        for obj in object_dicts:
            row = [str(obj[column]) for column in columns]
            table.add_row(*row)
        self.print(table)

    def display_table(self, title: str, columns: List[str], rows: List[Any]) -> None:
        """
        Display a table with specified columns and rows.

        Parameters
        ----------
        title : str
            The title of the table.
        columns : List[str]
            A list of column names.
        rows : List[List[Any]]
            A list of rows, where each row is a list of values.
        """
        table = Table(title=title, show_header=True)
        for column in columns:
            table.add_column(column, justify="right")
        for row in rows:
            row_values = [str(row[row_col_name]) for row_col_name in columns]
            table.add_row(*row_values)
        self.print(table)

    def display_error(self, error_message: str) -> None:
        """
        Display an error message.

        Parameters
        ----------
        error_message : str
            The error message to display.
        """
        self.print(f"[bold red]Error:[/bold red] {error_message}")

    def watch_console_log(self, log_output: str) -> None:
        """
        Display console log output in real-time.

        Parameters
        ----------
        log_output : str
            The log output to display.
        """
        with Live(console=self.config.console) as live:
            live.update(log_output)

    def display_dynamic_table(self, title: str, items: List[Any]) -> None:
        """
        Display a dynamic table based on the attributes of the items.

        Parameters
        ----------
        title : str
            The title of the table.
        items : List[Any]
            A list of objects to display in the table. Each object's attributes
            will be used as columns.
        """
        if not items:
            self.display_error("No items to display.")
            return

        table = Table(title=title, show_header=True)
        first_item = items[0]
        columns = [
            attr
            for attr in dir(first_item)
            if not attr.startswith("_") and not callable(getattr(first_item, attr))
        ]

        for column in columns:
            table.add_column(column.capitalize(), justify="right")

        for item in items:
            row = [str(getattr(item, column)) for column in columns]
            table.add_row(*row)

        self.print(table)

    def info(self, message: str) -> None:
        """
        Prints an informational message to the console using rich presentation if enabled.

        Parameters
        ----------
        message : str
            The message to be printed.
        """
        if self.config.logger:
            self.config.logger.info(message, extra={"markup": True})

    def error(self, message: str) -> None:
        """
        Prints an error message to the console using rich presentation if enabled.

        Parameters
        ----------
        message : str
            The message to be printed.
        """
        if self.config.logger:
            self.config.logger.error(
                f"[bold red]{message}[/bold red]", extra={"markup": True}
            )

    def warn(self, message: str) -> None:
        """
        Prints a warning message to the console using rich presentation if enabled.

        Parameters
        ----------
        message : str
            The message to be printed.
        """
        if self.config.logger:
            self.config.logger.warning(
                f"[bold yellow]{message}[/bold yellow]", extra={"markup": True}
            )

    def debug(self, message: str) -> None:
        """
        Prints a debug message to the console using rich presentation if enabled.

        Parameters
        ----------
        message : str
            The message to be printed.
        """
        if self.config.logger:
            self.config.logger.debug(
                f"[bold blue]{message}[/bold blue]", extra={"markup": True}
            )
