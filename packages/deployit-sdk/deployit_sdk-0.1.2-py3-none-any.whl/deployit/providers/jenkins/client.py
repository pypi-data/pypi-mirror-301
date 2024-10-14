from deployit.providers.jenkins.clients.http import RequestsHTTPClient
from deployit.providers.jenkins.clients.jenkins import JenkinsAPIClient
from deployit.providers.jenkins.models.url import JenkinsURLBuilder
from deployit.providers.jenkins.services.build import JenkinsBuildApiService
from deployit.providers.jenkins.services.common import JenkinsCommonApiService
from deployit.providers.jenkins.services.job import JenkinsJobApiService


class JenkinsClient:
    """
    JenkinsClient acts as an entry point to access various functionalities of the Jenkins client.

    Attributes
    ----------
    job_repository : JobRepository
        An instance of JobRepository to manage job-related operations.
    build_repository : BuildRepository
        An instance of BuildRepository to manage build-related operations.
    common_service : JenkinsCommonApiService
        An instance of JenkinsCommonApiService to manage common Jenkins API operations.
    build_service : JenkinsBuildApiService
        An instance of JenkinsBuildApiService to manage build-related Jenkins API operations.
    job_service : JenkinsJobApiService
        An instance of JenkinsJobApiService to manage job-related Jenkins API operations.
    presenter : RichPresenter
        An instance of RichPresenter to handle presentation logic.
    """

    def __init__(self):
        """
        Initializes the JenkinsClient with instances of repositories, services, and parameters.

        Parameters
        ----------
        base_url : str
            The base URL of the Jenkins server.
        username : str
            The username for authentication.
        password : str
            The password or API token for authentication.
        """
        url_builder = JenkinsURLBuilder()
        http_client = RequestsHTTPClient()

        self.jenkins_client = JenkinsAPIClient(url_builder, http_client)
        self.build = JenkinsBuildApiService(self.jenkins_client)
        self.job = JenkinsJobApiService(self.jenkins_client)
        self.common = JenkinsCommonApiService(self.jenkins_client)

    def set_base_url(self, base_url: str):
        """
        Set the base URL of the Jenkins server.

        Parameters
        ----------
        base_url : str
            The base URL of the Jenkins server.
        """
        self.jenkins_client.url_builder.base_url = base_url

    def get_common_service(self) -> JenkinsCommonApiService:
        """
        Get the JenkinsCommonApiService instance.

        Returns
        -------
        JenkinsCommonApiService
            The instance of JenkinsCommonApiService.
        """
        return self.common

    def get_build_service(self) -> JenkinsBuildApiService:
        """
        Get the JenkinsBuildApiService instance.

        Returns
        -------
        JenkinsBuildApiService
            The instance of JenkinsBuildApiService.
        """
        return self.build

    def get_job_service(self) -> JenkinsJobApiService:
        """
        Get the JenkinsJobApiService instance.

        Returns
        -------
        JenkinsJobApiService
            The instance of JenkinsJobApiService.
        """
        return self.job
