from deployit.providers.jenkins.clients.jenkins import JenkinsAPIClient


class JenkinsApiService:
    def __init__(self, jenkins_client: JenkinsAPIClient):
        """
        Initialize the JenkinsApiService with a Jenkins API client.

        Parameters
        ----------
        jenkins_client : JenkinsAPIClient
            The Jenkins API client instance.
        """
        self.jenkins_client = jenkins_client
