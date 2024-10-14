from typing import Any, Dict, List, Optional

from deployit.providers.jenkins.models.base import JenkinsObject
from deployit.providers.jenkins.models.build import Build


class Job(JenkinsObject):
    def __init__(self, job_info: Dict):
        """
        Initialize the JenkinsJob object with the provided job information.

        Parameters
        ----------
        job_info : dict
            The dictionary containing job information from Jenkins.
        """
        self.build_history: List[Build] = []  # Added type annotation
        self.extended_parameters: Dict[str, Any] = {}  # Added type annotation
        self.update(job_info)

    def update(self, job_info: Dict):
        """
        Update the JenkinsJob object with new information from the Jenkins API.

        Parameters
        ----------
        job_info : dict
            The dictionary containing job information from Jenkins.
        """
        self.full_name = job_info.get("fullName")
        self.name = job_info.get("name")
        self.url = job_info.get("url")
        self.url_path = job_info.get(
            "urlPath",
            "/"
            + "/".join(
                [
                    field
                    for field in job_info.get("url", "").split("/")
                    if field != "job"
                ][3:]
            ),
        )
        self.next_build_number = job_info.get("nextBuildNumber")
        self.concurrent_build = job_info.get("concurrentBuild")
        self.in_queue = job_info.get("inQueue")
        self.queue_item = job_info.get("queueItem")
        self.resume_blocked = job_info.get("resumeBlocked")
        self.buildable = job_info.get("buildable")
        self.extended_parameters = job_info.get("extended_parameters", {})
        self.required_parameters = self._get_required_parameters(
            job_info.get("property", [])
        )
        self.subjobs = self._parse_subjobs(job_info.get("jobs", []))

    def _parse_subjobs(self, subjobs: List[Dict]) -> List["Job"]:
        """
        Parse the subjobs from the job information.

        Parameters
        ----------
        subjobs : list of dict
            A list of dictionaries containing subjob information.

        Returns
        -------
        list of str
            A list of subjob names.
        """
        parsed_subjobs_list = []
        for job_info in subjobs:
            if (
                "jobs" in job_info
                and job_info.get("jobs") is not None
                or job_info.get("jobs") != []
            ):
                parsed_subjobs_list.append(Job(job_info))
        return parsed_subjobs_list

    def _get_required_parameters(self, properties: List[Dict]) -> List[Dict]:
        """
        Extract required parameters from the job properties.

        Parameters
        ----------
        properties : list of dict
            A list of properties associated with the Jenkins job.

        Returns
        -------
        list of dict
            A list of dictionaries containing required parameters.
        """
        required_parameters = []

        for prop in properties:
            if prop.get("_class") == "hudson.model.ParametersDefinitionProperty":
                for param in prop.get("parameterDefinitions", []):
                    param_info = self._extract_param_info(param)
                    if param_info:
                        required_parameters.append(param_info)
        return required_parameters

    def _extract_param_info(self, param: Dict) -> Optional[Dict]:
        """
        Extract information for a single parameter definition.

        Parameters
        ----------
        param : dict
            The dictionary containing parameter definition information.

        Returns
        -------
        dict, optional
            A dictionary containing the extracted parameter information, or None if the parameter type is not recognized.
        """
        param_name = param.get("name")
        param_description = param.get("description")
        param_type = param.get("_class")

        if param_type == "hudson.model.ChoiceParameterDefinition":
            param_choices = param.get("choices", [])
            return {
                "name": param_name,
                "description": param_description,
                "choices": param_choices,
            }
        elif param_type == "hudson.model.TextParameterDefinition":
            return {"name": param_name, "description": param_description}
        elif param_type == "hudson.plugins.git.GitParameterDefinition":
            param_values = param.get("allValueItems", {}).get("values", [])
            return {
                "name": param_name,
                "description": param_description,
                "values": param_values,
            }
        return None

    def get_parameter_options(self, parameter_path: str) -> Dict[str, Any]:
        """
        Get options for a specific parameter path.

        Parameters
        ----------
        parameter_path : str
            The path to the parameter, e.g., "01common.plataform"

        Returns
        -------
        Dict[str, Any]
            The options for the specified parameter path
        """
        keys = parameter_path.split(".")
        current = self.extended_parameters
        for key in keys:
            if key in current:
                current = current[key]
            else:
                return {}
        return current
