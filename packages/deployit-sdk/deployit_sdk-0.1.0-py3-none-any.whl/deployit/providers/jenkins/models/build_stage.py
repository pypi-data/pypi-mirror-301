from typing import Dict

from deployit.providers.jenkins.models.base import JenkinsObject
from deployit.providers.jenkins.utils.time import convert_duration, convert_timestamp


class JenkinsBuildStage(JenkinsObject):
    def __init__(self, stage_info: Dict):
        self.id = stage_info.get("id")
        self.build_id = stage_info.get("buildId")
        self.name = stage_info.get("name")
        self.status = stage_info.get("status")
        self.start_time = convert_timestamp(
            stage_info.get("startTimeMillis") or 0
        )  # Use 0 if None
        self.duration = convert_duration(
            stage_info.get("durationMillis") or 0
        )  # Use 0 if None
        self.pause_duration = convert_duration(
            stage_info.get("pauseDurationMillis") or 0
        )  # Use 0 if None
