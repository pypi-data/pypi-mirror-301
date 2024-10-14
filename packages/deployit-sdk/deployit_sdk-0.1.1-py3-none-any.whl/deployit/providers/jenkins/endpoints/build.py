class BuildEndpoints:
    """
    Endpoints related to builds in Jenkins.

    Attributes
    ----------
    BUILD_INFO : str
        URL template to get detailed information about a specific build.
    BUILD_CONSOLE_OUTPUT : str
        URL template to get the console output of a specific build.
    BUILD_ENV_VARS : str
        URL template to get the environment variables injected into a specific build.
    BUILD_TEST_REPORT : str
        URL template to get the test report of a specific build.
    BUILD_ARTIFACT : str
        URL template to get a specific artifact from a build.
    BUILD_STAGES : str
        URL template to get the stages of a specific build in a pipeline.
    STOP_BUILD : str
        URL template to stop a specific build.

    Notes
    -----
    These endpoints are used to interact with the Jenkins API to retrieve various details about builds.
    """

    BUILD_INFO: str = "{base_url}/{number}/api/json?depth={depth}"
    BUILD_CONSOLE_OUTPUT: str = "{base_url}/{number}/consoleText"
    BUILD_ENV_VARS: str = "{base_url}/{number}/injectedEnvVars/api/json?depth={depth}"
    BUILD_TEST_REPORT: str = "{base_url}/{number}/testReport/api/json?depth={depth}"
    BUILD_ARTIFACT: str = "{base_url}/{number}/artifact/{artifact}"
    BUILD_STAGES: str = "{base_url}/{number}/wfapi/describe/"
    STOP_BUILD: str = "{base_url}/{number}/stop"
