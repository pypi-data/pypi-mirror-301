from typing import Dict

from deployit.providers.jenkins.endpoints.common import CommonEndpoints
from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.services.base import JenkinsApiService
from deployit.providers.jenkins.utils.errors import JenkinsError


class JenkinsCommonApiService(JenkinsApiService):
    def __init__(self, jenkins_client):
        super().__init__(jenkins_client)
        self.presenter = RichPresenter()

    def get_jenkins_info(self) -> Dict:
        """
        Retrieve general information about the Jenkins instance.

        Returns
        -------
        dict
            The Jenkins instance information.
        """
        self.presenter.info("Retrieving Jenkins instance information.")
        try:
            response = self.jenkins_client.make_request(
                CommonEndpoints.INFO, method="GET"
            )
            self.presenter.info("Successfully retrieved Jenkins instance information.")
            return response
        except JenkinsError as e:
            self.presenter.error(f"Jenkins error retrieving instance information: {e}")
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving Jenkins instance information: {e}"
            )
            raise

    def get_crumb(self) -> Dict:
        """
        Retrieve a Jenkins crumb, used for CSRF protection.

        Returns
        -------
        dict
            The crumb information.
        """
        self.presenter.info("Retrieving Jenkins crumb for CSRF protection.")
        try:
            response = self.jenkins_client.make_request(
                CommonEndpoints.CRUMB_ISSUER, method="GET"
            )
            self.presenter.info("Successfully retrieved Jenkins crumb.")
            return response
        except JenkinsError as e:
            self.presenter.error(f"Jenkins error retrieving crumb: {e}")
            raise
        except Exception as e:
            self.presenter.error(f"Unexpected error retrieving Jenkins crumb: {e}")
            raise

    def who_am_i(self, depth: int = 1) -> Dict:
        """
        Retrieve the current user information.

        Parameters
        ----------
        depth : int, optional
            The depth of the information retrieval (default is 1).

        Returns
        -------
        dict
            The current user information.
        """
        self.presenter.info(f"Retrieving current user information with depth: {depth}.")
        try:
            response = self.jenkins_client.make_request(
                CommonEndpoints.WHOAMI_URL, method="GET", depth=depth
            )
            self.presenter.info("Successfully retrieved current user information.")
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving current user information: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving current user information: {e}"
            )
            raise
