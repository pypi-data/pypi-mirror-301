from typing import Dict

from deployit.providers.jenkins.clients.jenkins import JenkinsAPIClient
from deployit.providers.jenkins.endpoints.queue import QueueEndpoints
from deployit.providers.jenkins.models.queue import Queue, QueueItem
from deployit.providers.jenkins.services.base import JenkinsApiService


class QueueApiService(JenkinsApiService):
    def __init__(self, jenkins_client: JenkinsAPIClient):
        """
        Initialize the QueueApiService with a JenkinsAPIClient.

        Parameters
        ----------
        jenkins_client : JenkinsAPIClient
            The Jenkins API client instance.
        """
        self.jenkins_client = jenkins_client

    def get_queue(self) -> Queue:
        """
        Retrieve the entire queue for a specific job.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.

        Returns
        -------
        Queue
            The Queue object containing all queued items.
        """
        queue_info = self.jenkins_client.make_request(
            QueueEndpoints.QUEUE_INFO,
            method="GET",
        )
        return Queue(queue_info)

    def get_queue_item(self, item_id: int) -> QueueItem:
        """
        Retrieve a specific queue item by its ID.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        item_id : int
            The ID of the queue item.

        Returns
        -------
        QueueItem
            The QueueItem object.
        """
        queue_item_info = self.jenkins_client.make_request(
            QueueEndpoints.QUEUE_ITEM,
            method="GET",
            number=item_id,
        )
        return QueueItem(
            id=queue_item_info["id"],
            task_name=queue_item_info["task"]["name"],
            url=queue_item_info["task"]["url"],
            buildable=queue_item_info.get("buildable", False),
            params=queue_item_info.get("params", None),
            why=queue_item_info.get("why", None),
            build_id=queue_item_info.get("executable", {}).get("number", None),
        )

    def cancel_queue_item(self, item_id: int) -> Dict:
        """
        Cancel a specific queue item by its ID.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        item_id : int
            The ID of the queue item to cancel.

        Returns
        -------
        dict
            The response from Jenkins after cancelling the queue item.
        """
        return self.jenkins_client.make_request(
            QueueEndpoints.CANCEL_QUEUE,
            method="POST",
            id=item_id,
        )
