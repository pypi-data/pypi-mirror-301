"""
This module provides a service for interacting with Jenkins jobs.
"""

import json
import re
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from bs4 import BeautifulSoup

from deployit.providers.jenkins.endpoints.job import JobEndpoints
from deployit.providers.jenkins.models.build import Build
from deployit.providers.jenkins.models.job import Job
from deployit.providers.jenkins.parameters.base import DeployParameters
from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.services.base import JenkinsApiService
from deployit.providers.jenkins.services.build import JenkinsBuildApiService
from deployit.providers.jenkins.services.utils_job import (
    JsonSchemaProcessor,
    JsonTransformer,
)
from deployit.providers.jenkins.utils.config import Config
from deployit.providers.jenkins.utils.errors import JenkinsAPIError
from deployit.providers.jenkins.utils.filter import matches_filter


class JenkinsJobApiService(JenkinsApiService):
    """
    A service class for interacting with Jenkins jobs.
    """

    def __init__(
        self, jenkins_client, build_service: Optional[JenkinsBuildApiService] = None
    ):
        super().__init__(jenkins_client)
        self.build_service = build_service or JenkinsBuildApiService(jenkins_client)
        self.presenter = RichPresenter()

    def get_all(self, tree: str) -> Dict:
        """
        Retrieve all jobs information with a specific tree structure.

        Parameters
        ----------
        tree : str
            The tree structure for retrieving job information.

        Returns
        -------
        dict
            Information about all jobs.
        """
        self.presenter.info(f"Retrieving all jobs with tree structure: {tree}")
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.JOBS_QUERY, method="GET", tree=tree
            )
            self.presenter.info("Successfully retrieved all jobs.")
            return response
        except Exception as e:
            self.presenter.error(f"Error retrieving all jobs: {e}")
            raise

    def get_info(self, base_url: str, depth: int = 1) -> Job:
        """
        Retrieve information about a specific job.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.
        depth : int, optional
            The depth of the information retrieval (default is 1).

        Returns
        -------
        Job
            The job information.
        """
        self.presenter.info(f"Retrieving job info for {base_url} with depth {depth}")
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.JOB_INFO,
                method="GET",
                base_url=base_url,
                depth=depth,
            )
            extended_response: Optional[Dict[str, Any]] = None
            if "ExtendedChoiceParameterDefinition" in json.dumps(response):
                extended_response = self._get_extended_parameters(base_url)
            job = Job(
                {
                    "extended_parameters": extended_response,
                    **response,
                    "urlPath": base_url,
                }
            )
            self.presenter.info("Successfully retrieved job info.")
            return job
        except Exception as e:
            self.presenter.error(f"Error retrieving job info: {e}")
            raise

    def wait_for_build(
        self, build_obj: Build, timeout: int = 120, interval: int = 10
    ) -> Build:
        """
        Wait for a build to start and return the Build object.

        Parameters
        ----------
        build_obj : Build
            The Build object to refresh.
        timeout : int
            The maximum time to wait for the build to start, in seconds.
        interval : int
            The interval between checks, in seconds.

        Returns
        -------
        Build
            The Build object once the build starts.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                build_obj = self.build_service.refresh_build(build_obj)
                if build_obj.number:
                    self.presenter.info(f"Build {build_obj.number} started.")
                    return build_obj
            except Exception as e:
                self.presenter.error(f"Error checking queue item: {e}")
            time.sleep(interval)
        raise TimeoutError(f"Build did not start within {timeout} seconds.")

    def build(
        self,
        base_url: str,
        params: Optional[Dict[str, Any]] = None,
        extended: bool = False,
        wait_until_start: bool = False,
        timeout: int = 120,
        interval: int = 10,
    ) -> Build:
        """
        Trigger a build for a specific job, with optional parameters and extended processing.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.
        params : dict, optional
            The parameters to pass to the job. If provided, a parameterized build is triggered.
            If `extended` is True, extended processing is applied to the parameters.
            By default, None.
        extended : bool, optional
            Whether to use extended parameter processing (default is False).
        wait_until_start : bool, optional
            Whether to wait until the build starts after triggering, in seconds (default is False).
        timeout : int, optional
            The maximum time to wait for the build to start, in seconds (default is 120).
        interval : int, optional
            The interval between checks while waiting for the build to start, in seconds (default is 10).

        Returns
        -------
        Build
            The Build object representing the triggered build.

        Raises
        ------
        JenkinsAPIError
            If an error occurs while triggering the build or processing parameters.
        TimeoutError
            If waiting for the build to start times out.
        """
        if params is None:
            params = {}

        if extended and params:
            return self._build_with_extended_params(
                base_url=base_url,
                params=params,
                wait_until_start=wait_until_start,
                timeout=timeout,
                interval=interval,
            )
        elif params:
            return self._build_with_params(
                base_url=base_url,
                params=params,
                wait_until_start=wait_until_start,
                timeout=timeout,
                interval=interval,
            )
        else:
            return self._build_simple(
                base_url=base_url,
                wait_until_start=wait_until_start,
                timeout=timeout,
                interval=interval,
            )

    def _build_simple(
        self,
        base_url: str,
        wait_until_start: bool = False,
        timeout: int = 120,
        interval: int = 10,
    ) -> Build:
        """
        Trigger a simple build for a specific job without parameters.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.
        wait_until_start : bool, optional
            Whether to wait until the build starts after triggering, in seconds (default is False).
        timeout : int, optional
            The maximum time to wait for the build to start, in seconds (default is 120).
        interval : int, optional
            The interval between checks while waiting for the build to start, in seconds (default is 10).

        Returns
        -------
        Build
            The Build object representing the triggered build.

        Raises
        ------
        JenkinsAPIError
            If an error occurs while triggering the build.
        TimeoutError
            If waiting for the build to start times out.
        """
        self.presenter.info(f"Triggering build for job {base_url}")
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.BUILD_JOB,
                method="POST",
                base_url=base_url,
            )
            self.presenter.info("Successfully triggered build.")
            if "Location" in response and "queue" in response["Location"]:
                queue_id = int(response["Location"].split("/")[-2])
                response["queueId"] = queue_id
            build_obj = Build({**response, "urlPath": base_url})
            if wait_until_start:
                build_obj = self.wait_for_build(build_obj, timeout, interval)
            return build_obj
        except Exception as e:
            self.presenter.error(f"Error triggering build: {e}")
            raise JenkinsAPIError(f"Error triggering build: {e}") from e

    def _build_with_params(
        self,
        base_url: str,
        params: Dict[str, Any],
        wait_until_start: bool = False,
        timeout: int = 120,
        interval: int = 10,
    ) -> Build:
        """
        Trigger a build for a specific job with parameters.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.
        params : dict
            The parameters to pass to the job.
        wait_until_start : bool, optional
            Whether to wait until the build starts after triggering, in seconds (default is False).
        timeout : int, optional
            The maximum time to wait for the build to start, in seconds (default is 120).
        interval : int, optional
            The interval between checks while waiting for the build to start, in seconds (default is 10).

        Returns
        -------
        Build
            The Build object representing the triggered build.

        Raises
        ------
        JenkinsAPIError
            If an error occurs while triggering the build with parameters.
        TimeoutError
            If waiting for the build to start times out.
        """
        self.presenter.info(
            f"Triggering build with parameters for job {base_url} with params {params}"
        )
        try:
            request_query = DeployParameters(**params).to_url_query()
            response = self.jenkins_client.make_request(
                JobEndpoints.BUILD_WITH_PARAMETERS,
                method="POST",
                query=request_query,
                base_url=base_url,
            )
            self.presenter.info("Successfully triggered build with parameters.")
            if "Location" in response and "queue" in response["Location"]:
                queue_id = int(response["Location"].split("/")[-2])
                response["queueId"] = queue_id
            build_obj = Build({**response, "urlPath": base_url})
            if wait_until_start:
                build_obj = self.wait_for_build(build_obj, timeout, interval)
            return build_obj
        except Exception as e:
            self.presenter.error(f"Error triggering build with parameters: {e}")
            raise JenkinsAPIError(f"Error triggering build with parameters: {e}") from e

    def _build_with_extended_params(
        self,
        base_url: str,
        params: Dict[str, Any],
        wait_until_start: bool = False,
        timeout: int = 120,
        interval: int = 10,
    ) -> Build:
        """
        Trigger a build for a specific job with extended parameters, including default values for unspecified parameters.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.
        params : dict
            The parameters to pass to the job. These will override default values.
        wait_until_start : bool, optional
            Whether to wait until the build starts after triggering, in seconds (default is False).
        timeout : int, optional
            The maximum time to wait for the build to start, in seconds (default is 120).
        interval : int, optional
            The interval between checks while waiting for the build to start, in seconds (default is 10).

        Returns
        -------
        Build
            The Build object representing the triggered build.

        Raises
        ------
        JenkinsAPIError
            If an error occurs while triggering the build with extended parameters.
        TimeoutError
            If waiting for the build to start times out.
        """
        self.presenter.info(
            f"Triggering build with extended parameters for job {base_url}"
        )
        try:
            # Define field-specific transformations
            transformations = {
                "root[05kubernetes][service][type]": lambda x: (
                    x.lower() if isinstance(x, str) else x
                ),
                "root[09test][reportType]": lambda x: "html" if x == "Chrome" else x,
                "root[01common][pcat]": lambda x: str(x) if isinstance(x, int) else x,
            }
            schema = self._get_extended_parameters(base_url)
            processor = JsonSchemaProcessor(schema=schema["schema"])
            validated_data = processor.validate_and_process(params)
            transformer = JsonTransformer(transformations=transformations)
            request_payload = transformer.transform(validated_data)
            self.jenkins_client.make_request(
                JobEndpoints.BUILD_JOB,
                method="POST",
                base_url=base_url,
                data=request_payload,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "Upgrade-Insecure-Requests": "1",
                },
                is_json=False,
            )
            time.sleep(15)  # takes a while to build
            job = self.get_info(base_url)
            build_obj = self.fetch_builds(
                job, filter_by={"actions.causes.userId": str(Config.USERNAME)}
            )[0]
            self.presenter.info(
                "Successfully triggered build with extended parameters."
            )
            if wait_until_start:
                build_obj = self.wait_for_build(build_obj, timeout, interval)
            return build_obj
        except Exception as e:
            self.presenter.error(
                f"Error triggering build with extended parameters: {e}"
            )
            raise JenkinsAPIError(
                f"Error triggering build with extended parameters: {e}"
            ) from e

    def get_all_builds(self, base_url: str) -> Dict:
        """
        Retrieve all builds information for a specific job with a specific tree structure.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.

        Returns
        -------
        dict
            Information about all builds for the job.
        """
        self.presenter.info(f"Retrieving all builds for job {base_url}.")
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.ALL_BUILDS,
                method="GET",
                base_url=base_url,
            )
            self.presenter.info("Successfully retrieved all builds.")
            return response
        except Exception as e:
            self.presenter.error(f"Error retrieving all builds: {e}")
            raise

    def fetch_job_details(self, job: Job) -> Job:
        """
        Fetch details for a given job and update the job instance.

        Parameters
        ----------
        job : Job
            The job for which to fetch details.

        Returns
        -------
        Job
            The updated job instance.
        """
        self.presenter.info(
            f"Fetching details for job '{job.name}' with URL '{job.url}'"
        )
        try:
            if not job.full_name:
                raise ValueError("Job full_name cannot be None")
            job_info = self.get_info(base_url=job.full_name)
            job = job_info  # Direct assignment instead of Job(job_info)
            job.build_history = self.fetch_builds(job)
            self.presenter.info(f"Successfully fetched details for job '{job.name}'")
        except Exception as e:
            raise JenkinsAPIError(f"Error fetching job details: {e}") from e
        return job

    def fetch_builds(self, job: Job, filter_by: Dict[str, Any] = {}) -> List[Build]:
        """
        Fetch all builds for a given job.

        Parameters
        ----------
        job : Job
            The job for which to fetch builds.
        filter_by : dict
            A dictionary of filters to apply to the builds.
            The key is the field to filter by, and the value is the value to filter for.

        Returns
        -------
        list
            A list of builds associated with the job.
        """
        self.presenter.info(
            f"Fetching all builds for job '{job.name}' with URL '{job.url}'"
        )
        try:
            builds_data = self.get_all_builds(base_url=job.url_path).get(
                "allBuilds", []
            )
            filtered_builds: List[Build] = []
            for build_response in builds_data:
                if matches_filter(build_response, filter_by):
                    filtered_builds.append(Build(build_response))
            self.presenter.info(
                f"Fetched {len(filtered_builds)} builds for job '{job.name}'"
            )
            return filtered_builds
        except Exception as e:
            raise JenkinsAPIError(
                f"Error fetching builds for job '{job.name}': {e}"
            ) from e

    def _get_extended_parameters(self, base_url: str) -> Dict[str, Any]:
        """
        Retrieve extended parameters for a job.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.

        Returns
        -------
        Dict[str, Any]
            The extended parameters for the job.
        """
        self.presenter.info(f"Retrieving extended parameters for job {base_url}")
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.BUILD_JOB,
                method="GET",
                base_url=base_url,
            )
            extended_params = self._parse_extended_parameters_from_html(response)
            self.presenter.info("Successfully retrieved extended parameters.")
            return extended_params
        except Exception as e:
            self.presenter.error(f"Error retrieving extended parameters: {e}")
            raise

    def _parse_json_object(self, s: str) -> Tuple[Dict[str, Any], int]:
        """
        Parse a string until it completes a whole JSON object.

        Parameters
        ----------
        s : str
            The string to parse.

        Returns
        -------
        Tuple[Dict[str, Any], int]
            A tuple containing the parsed JSON object and the index where parsing ended.
        """
        stack: List[str] = []
        in_string: bool = False
        escape: bool = False
        start: Optional[int] = None

        for i, char in enumerate(s):
            if char == '"' and not escape:
                in_string = not in_string
            elif not in_string:
                if char == "{":
                    if not stack:
                        start = i
                    stack.append(char)
                elif char == "}":
                    if stack and stack[-1] == "{":
                        stack.pop()
                        if not stack:
                            try:
                                return json.loads(s[start : i + 1]), i + 1
                            except json.JSONDecodeError:
                                continue
                    else:
                        # Mismatched brackets, reset
                        stack = []
                        start = None

            escape = char == "\\" and not escape

        raise ValueError("No valid JSON object found")

    def _parse_extended_parameters_from_html(
        self, response: Union[str, Dict[str, Any], bytes]
    ) -> Dict[str, Any]:
        """
        Parse extended parameters from HTML content.

        Parameters
        ----------
        response : Union[str, Dict[str, Any], bytes]
            The HTML content of the build page.

        Returns
        -------
        Dict[str, Any]
            The parsed extended parameters.
        """
        try:
            if isinstance(response, dict):
                # If response is already a dictionary, try to extract 'content' key
                html_content = response.get("content", "")
            elif isinstance(response, (str, bytes)):
                html_content = response
            else:
                raise ValueError(f"Unexpected response type: {type(response)}")

            if not html_content:
                raise ValueError("Empty HTML content")
            soup = BeautifulSoup(html_content, "html.parser")
            script_content = soup.find("script", text=re.compile("JSONEditor"))
            if not script_content:
                raise ValueError("Could not find JSONEditor script in HTML content")
            json_match = re.search(
                r"JSONEditor\(.+?, (\{.+\})\);", script_content.string, re.DOTALL
            )
            if not json_match:
                raise ValueError("Could not find JSON schema in script content")
            json_str = json_match.group(1)
            json_schema, _ = self._parse_json_object(json_str)
            if "schema" not in json_schema:
                raise ValueError("Invalid JSON schema structure")
            return json_schema
        except Exception as e:
            self.presenter.error(f"Error parsing extended parameters: {e}")
            return {}  # Return an empty dict if parsing fails
