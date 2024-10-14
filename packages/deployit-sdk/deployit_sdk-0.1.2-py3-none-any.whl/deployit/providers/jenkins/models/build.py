from typing import Any, Dict

from deployit.providers.jenkins.models.base import JenkinsObject
from deployit.providers.jenkins.utils.time import convert_duration, convert_timestamp


class Build(JenkinsObject):
    def __init__(self, build_info):
        self.update(build_info)
        self.console_log: Any = None

    def update(self, build_info: Dict):
        """
        Update the Build object with new information from the Jenkins API.

        Parameters
        ----------
        build_info : dict
            The dictionary containing build information from Jenkins.
        """
        self.sonar_link = self._get_sonar_link(build_info)
        self.cause = self._get_cause(build_info)
        self.is_building = build_info.get("building", False)
        self.description = build_info.get("description", None)
        self.duration = convert_duration(build_info.get("duration", 0))
        self.estimated_duration = convert_duration(
            build_info.get("estimatedDuration", 0)
        )
        self.id = build_info.get("id", None)
        self.keep_log = build_info.get("keepLog", False)
        self.number = build_info.get("number", None)
        self.queue_id = build_info.get("queueId", None)
        self.result = build_info.get("result", None)
        self.timestamp = convert_timestamp(build_info.get("timestamp", 0))
        self.in_progress = build_info.get("inProgress", False)
        self.url = build_info.get("url", None)
        self.url_path = build_info.get(
            "urlPath",
            "/"
            + "/".join(
                [
                    field
                    for field in build_info.get("url", "").split("/")
                    if field != "job"
                ][3:-2]
            ),
        )

        # Optionally update other attributes like stages and console log if needed
        if "stages" in build_info:
            self.stages = build_info["stages"]
        if "console_log" in build_info:
            self.console_log = build_info["console_log"]

    def _get_sonar_link(self, json_data):
        """
        Get the SonarQube dashboard URL from the build JSON data.

        Parameters
        ----------
        json_data : dict
            The JSON data of the build.

        Returns
        -------
        str
            The SonarQube dashboard URL.
        """
        for action in json_data.get("actions", []):
            if (
                action.get("_class")
                == "hudson.plugins.sonar.action.SonarAnalysisAction"
            ):
                return action.get("sonarqubeDashboardUrl")
        return None

    def _get_cause(self, json_data):
        """
        Get the cause of the build from the build JSON data.

        Parameters
        ----------
        json_data : dict
            The JSON data of the build.

        Returns
        -------
        dict
            The cause of the build.
        """
        filtered_cause = None
        for action in json_data.get("actions", []):
            if action.get("_class") == "hudson.model.CauseAction":
                for cause in action.get("causes", []):
                    if cause.get("_class") == "jenkins.branch.BranchEventCause":
                        filtered_cause = self._get_branch_event_cause(json_data)
                    elif cause.get("_class") == "hudson.model.Cause$UserIdCause":
                        filtered_cause = {
                            "userId": cause.get("userId"),
                            "userName": cause.get("userName"),
                        }
        return filtered_cause

    def _get_branch_event_cause(self, json_data):
        """
        Get the cause of the build from the build JSON data.

        Parameters
        ----------
        json_data : dict
            The JSON data of the build.

        Returns
        -------
        dict
            The cause of the build.
        """
        cause_info = {
            "remoteUrls": [],
            "affectedPaths": [],
            "commitId": None,
            "authorFullName": None,
            "authorEmail": None,
            "date": None,
            "msg": None,
            "editTypes": [],
        }

        for action in json_data.get("actions", []):
            if action.get("_class") == "hudson.plugins.git.util.BuildData":
                cause_info["remoteUrls"] = action.get("remoteUrls", [])

        for change_set in json_data.get("changeSets", []):
            if change_set.get("_class") == "hudson.plugins.git.GitChangeSetList":
                for item in change_set.get("items", []):
                    cause_info["commitId"] = item.get("commitId")
                    cause_info["authorFullName"] = item.get("author", {}).get(
                        "fullName"
                    )
                    cause_info["authorEmail"] = item.get("authorEmail")
                    cause_info["date"] = item.get("date")
                    cause_info["msg"] = item.get("msg")
                    cause_info["affectedPaths"] = item.get("affectedPaths", [])
                    for path in item.get("paths", []):
                        cause_info["editTypes"].append(
                            {"file": path.get("file"), "editType": path.get("editType")}
                        )
        return cause_info
