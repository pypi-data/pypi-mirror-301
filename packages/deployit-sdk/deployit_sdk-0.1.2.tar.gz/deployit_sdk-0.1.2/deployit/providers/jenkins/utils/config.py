import os


class Config:
    """
    Configuration settings for the Jenkins API library.

    Attributes
    ----------
    JENKINS_DOMAIN : str
        The base URL for the Jenkins server.
    USERNAME : str
        The username for authenticating with Jenkins.
    API_TOKEN : str
        The API token for authenticating with Jenkins.
    TIMEOUT : int
        Timeout duration for API requests.
    """

    JENKINS_CRUMB = os.getenv("JENKINS_CRUMB", "jenkins-crumb")
    JENKINS_DOMAIN = os.getenv("JENKINS_DOMAIN", "localhost")
    USERNAME = os.getenv("JENKINS_USERNAME", "your-username")
    API_TOKEN = os.getenv("JENKINS_API_TOKEN", "your-api-token")
    TIMEOUT = int(os.getenv("JENKINS_TIMEOUT", "15"))
