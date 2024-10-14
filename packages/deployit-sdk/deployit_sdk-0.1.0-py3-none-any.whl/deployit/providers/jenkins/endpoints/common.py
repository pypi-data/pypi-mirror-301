class CommonEndpoints:
    """
    Common endpoints for Jenkins.

    Attributes
    ----------
    CRUMB_ISSUER : str
        URL template to get the crumb issuer for CSRF protection.
    INFO : str
        URL template to get general information about the Jenkins instance.
    WHOAMI_URL : str
        URL template to get information about the current user.
    """

    CRUMB_ISSUER: str = "crumbIssuer/api/json"
    INFO: str = "api/json"
    WHOAMI_URL: str = "me/api/json?depth={depth}"


COMMON_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Host": "jenkins.mgt.naturabanking.com",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Content-Type": "text/xml; charset=utf-8",
}
