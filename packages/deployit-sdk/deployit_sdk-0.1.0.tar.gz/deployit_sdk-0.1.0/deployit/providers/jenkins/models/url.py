from dataclasses import dataclass
from typing import Optional

from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.utils.config import Config


@dataclass
class JenkinsCrumb:
    crumb: str


@dataclass
class JenkinsURLBuilder:
    base_url: Optional[str] = Config.JENKINS_DOMAIN
    presenter: Optional[RichPresenter] = None

    def __post_init__(self):
        if self.presenter is None:
            self.presenter = RichPresenter()

    def build_url(self, endpoint_template: str, **kwargs) -> str:
        """
        Build a complete URL for a Jenkins API endpoint.

        Parameters
        ----------
        endpoint_template : str
            The template of the endpoint URL.
        kwargs : dict
            Additional parameters to format the endpoint template.

        Returns
        -------
        str
            The complete URL.
        """
        if self.presenter:
            self.presenter.debug(f"Building URL with template: {endpoint_template}")
            self.presenter.debug(f"Using base URL: {self.base_url}")
            self.presenter.debug(f"Additional parameters: {kwargs}")
        url_path = kwargs.get("base_url", "")
        if url_path or "/job/" not in url_path:
            kwargs["base_url"] = "/job/".join(url_path.split("/"))
        else:
            kwargs["base_url"] = url_path
        try:
            endpoint = endpoint_template.format(**kwargs)
            if "query" in kwargs.keys() and len(kwargs["query"]) > 2:
                endpoint = f"{endpoint}?{kwargs['query']}"
            self.complete_url = f"{self.base_url}{endpoint}"
            if self.presenter:
                self.presenter.debug(f"Successfully built URL: {self.complete_url}")
            return self.complete_url
        except KeyError as e:
            if self.presenter:
                self.presenter.error(f"Missing parameter for URL template: {e}")
            raise
        except Exception as e:
            if self.presenter:
                self.presenter.error(f"Error building URL: {e}")
            raise
