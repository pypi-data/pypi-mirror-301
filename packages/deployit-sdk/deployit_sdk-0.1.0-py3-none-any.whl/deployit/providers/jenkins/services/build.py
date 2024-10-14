from typing import Dict, Optional

from deployit.providers.jenkins.clients.jenkins import JenkinsAPIClient
from deployit.providers.jenkins.endpoints.build import BuildEndpoints
from deployit.providers.jenkins.models.build import Build
from deployit.providers.jenkins.models.build_stage import JenkinsBuildStage
from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.services.base import JenkinsApiService
from deployit.providers.jenkins.services.queue import QueueApiService
from deployit.providers.jenkins.utils.errors import JenkinsError


class JenkinsBuildApiService(JenkinsApiService):
    def __init__(
        self,
        jenkins_client: JenkinsAPIClient,
        queue_service: Optional[QueueApiService] = None,
    ):
        super().__init__(jenkins_client)
        self.queue_service = queue_service or QueueApiService(jenkins_client)
        self.presenter = RichPresenter()

    def refresh_build(self, build: Build):
        """
        Refresh the build information until it starts executing.

        Parameters
        ----------
        build : Build
            The Build object to refresh.
        """
        if build.queue_id:
            queue_item = self.queue_service.get_queue_item(int(build.queue_id))
            if queue_item.buildable or queue_item.why is None:
                build_info = self.jenkins_client.make_request(
                    BuildEndpoints.BUILD_INFO,
                    method="GET",
                    base_url=build.url_path,
                    number=queue_item.build_id,
                    depth=1,
                )
                build.update(build_info)
                self.presenter.info(
                    f"Build {build.number} for job {build.url_path} has started and updated."
                )
            else:
                self.presenter.info(
                    f"Build is still in the queue.\nReason: {queue_item.why}"
                )
            return build
        else:
            raise ValueError("Build is not queued, cannot refresh.")

    @staticmethod
    def extract_job_info(url: str) -> tuple:
        """
        Extract the folder URL and job short name from a job URL.

        Parameters
        ----------
        url : str
            The URL of the job.

        Returns
        -------
        tuple
            A tuple containing the folder URL and job short name.
        """
        parts = url.split("/")
        folder_url = "/".join(parts[:-2]) + "/"
        short_name = parts[-2]
        return folder_url, short_name

    def stop(self, base_url: str, number: int) -> Dict:
        """
        Stop a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to stop.

        Returns
        -------
        dict
            The response from stopping the build.
        """
        self.presenter.info(f"Stopping build {number} for job {base_url}.")
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.STOP_BUILD,
                method="POST",
                base_url=base_url,
                number=number,
            )

            self.presenter.info(
                f"Successfully stopped build {number} for job {base_url}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error stopping build {number} for job {base_url}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error stopping build {number} for job {base_url}: {e}"
            )
            raise

    def get_build_info(
        self,
        base_url: str,
        number: int,
        depth: int = 1,
        with_stages=True,
        with_console_log=False,
    ) -> Build:
        """
        Retrieve information about a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve information about.
        depth : int, optional
            The depth of the information retrieval (default is 1).
        with_stages : bool, optional
            Whether to retrieve stages information (default is True).
        with_console_log : bool, optional
            Whether to retrieve console output information (default is False).

        Returns
        -------
        dict
            The build information.
        """
        self.presenter.info(
            f"Retrieving information for build {number} of job {base_url} with depth {depth}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_INFO,
                method="GET",
                base_url=base_url,
                number=number,
                depth=depth,
            )
            self.presenter.info(
                f"Successfully retrieved information for build {number} of job {base_url}."
            )
            self.object = Build({**response, "urlPath": base_url})
            if with_stages:
                self.object.stages = self.get_stages(base_url, number)
            if with_console_log:
                self.object.console_log = str(
                    self.get_console_log(base_url, number).get("content", "")
                )
            return self.object
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving information for build {number} of job {base_url}: {e}"
            )
            raise

    def get_console_log(self, base_url: str, number: int) -> Dict:
        """
        Retrieve the console output of a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve console output for.

        Returns
        -------
        dict
            The build console output.
        """
        self.presenter.info(
            f"Retrieving console output for build {number} of job {base_url}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_CONSOLE_OUTPUT,
                method="GET",
                base_url=base_url,
                number=number,
                is_json=False,
            )
            self.presenter.info(
                f"Successfully retrieved console output for build {number} of job {base_url}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving console output for build {number} of job {base_url}: {e}"
            )
            raise

    def get_env_vars(self, base_url: str, number: int, depth: int = 1) -> Dict:
        """
        Retrieve the environment variables of a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve environment variables for.
        depth : int, optional
            The depth of the information retrieval (default is 1).

        Returns
        -------
        dict
            The environment variables of the build.
        """
        self.presenter.info(
            f"Retrieving environment variables for build {number} of job {base_url} with depth {depth}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_ENV_VARS,
                method="GET",
                base_url=base_url,
                number=number,
                depth=depth,
            )
            self.presenter.info(
                f"Successfully retrieved environment variables for build {number} of job {base_url}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving environment variables for build {number} of job {base_url}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving environment variables for build {number} of job {base_url}: {e}"
            )
            raise

    def get_test_report(self, base_url: str, number: int, depth: int = 1) -> Dict:
        """
        Retrieve the test report of a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve the test report for.
        depth : int, optional
            The depth of the information retrieval (default is 1).

        Returns
        -------
        dict
            The test report of the build.
        """
        self.presenter.info(
            f"Retrieving test report for build {number} of job {base_url} with depth {depth}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_TEST_REPORT,
                method="GET",
                base_url=base_url,
                number=number,
                depth=depth,
            )
            self.presenter.info(
                f"Successfully retrieved test report for build {number} of job {base_url}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving test report for build {number} of job {base_url}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving test report for build {number} of job {base_url}: {e}"
            )
            raise

    def get_artifact(self, base_url: str, number: int, artifact: str) -> Dict:
        """
        Retrieve a specific artifact from a build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve the artifact from.
        artifact : str
            The artifact path.

        Returns
        -------
        dict
            The artifact data.
        """
        self.presenter.info(
            f"Retrieving artifact {artifact} for build {number} of job {base_url}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_ARTIFACT,
                method="GET",
                base_url=base_url,
                number=number,
                artifact=artifact,
            )
            self.presenter.info(
                f"Successfully retrieved artifact {artifact} for build {number} of job {base_url}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving artifact {artifact} for build {number} of job {base_url}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving artifact {artifact} for build {number} of job {base_url}: {e}"
            )
            raise

    def get_pending_stages(self, base_url: str, number: int, show_data=True) -> list:
        """
        Retrieve the pending stages of a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.

        short_name : str
            The short name of the job.

        number : int
            The build number to retrieve pending stages for.

        Returns
        -------
        dict
            The build pending stages information.
        """
        self.presenter.info(
            f"Retrieving pending stages for build {number} of job {base_url}."
        )
        try:
            stages = self.get_stages(base_url, number, show_data=False)
            pending_stages = [
                stage
                for stage in stages
                if stage.status in ("PAUSED_PENDING_INPUT", "PAUSED_PENDING_APPROVAL")
            ]
            if show_data:
                self.presenter.display_jenkins_objects(
                    f"Job: {base_url} - Build: {number} ",
                    pending_stages,
                )
            return pending_stages
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving pending stages for build {number} of job {base_url}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving pending stages for build {number} of job {base_url}: {e}"
            )
            raise

    def get_stages(self, base_url: str, number: int, show_data=True) -> list:
        """
        Retrieve the stages of a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve stages for.

        Returns
        -------
        dict
            The build stages information.
        """
        self.presenter.info(f"Retrieving stages for build {number} of job {base_url}.")
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_STAGES,
                method="GET",
                base_url=base_url,
                number=number,
            )
            stages = [
                JenkinsBuildStage({**stage_info, "buildId": number})
                for stage_info in response.get("stages", [])
            ]
            if show_data:
                self.presenter.display_jenkins_objects(
                    f"Job: {base_url} - Build: {number} ",
                    stages,
                )
            self.presenter.info(
                f"Successfully retrieved stages for build {number} of job {base_url}."
            )
            return stages
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving stages for build {number} of job {base_url}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving stages for build {number} of job {base_url}: {e}"
            )
            raise

    def fetch_status(self, build: Build, base_url: str) -> str:
        """
        Fetch the status of a given build.

        Parameters
        ----------
        build : Build
            The build object.
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.

        Returns
        -------
        str
            The status of the build.
        """
        self.presenter.info(
            f"Fetching status for build {build.number} of job {base_url}."
        )
        try:
            build_info: Build = self.get_build_info(base_url, build.number)
            status = build_info.result
            self.presenter.info(
                f"Successfully fetched status for build {build.number} of job {base_url}: {status}"
            )
            return status
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error fetching status for build {build.number} of job {base_url}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error fetching status for build {build.number} of job {base_url}: {e}"
            )
            raise
