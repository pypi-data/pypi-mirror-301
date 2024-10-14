from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class QueueItem:
    id: int
    task_name: str
    url: str
    buildable: bool
    params: Optional[Dict] = None
    why: Optional[str] = None
    build_id: Optional[int] = None


class Queue:
    def __init__(self, queue_info: Dict):
        """
        Initialize the Queue object with queue information.

        Parameters
        ----------
        queue_info : dict
            The raw JSON data retrieved from Jenkins queue endpoint.
        """
        self.items = self._parse_queue_info(queue_info)

    def _parse_queue_info(self, queue_info: Dict) -> List[QueueItem]:
        """
        Parse the raw queue information into a list of QueueItems.

        Parameters
        ----------
        queue_info : dict
            The raw JSON data retrieved from Jenkins queue endpoint.

        Returns
        -------
        list
            A list of QueueItems.
        """
        items = []
        for item in queue_info.get("items", []):
            queue_item = QueueItem(
                id=item["id"],
                task_name=item["task"]["name"],
                url=item["task"]["url"],
                buildable=item.get("buildable", False),
                params=item.get("params", None),
                why=item.get("why", None),
                build_id=item.get("executable", {}).get("number", None),
            )
            items.append(queue_item)
        return items

    def get_item_by_id(self, item_id: int) -> Optional[QueueItem]:
        """
        Retrieve a specific QueueItem by its ID.

        Parameters
        ----------
        item_id : int
            The ID of the queue item.

        Returns
        -------
        QueueItem or None
            The QueueItem with the given ID, or None if not found.
        """
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def is_item_executable(self, item_id: int) -> bool:
        """
        Check if a specific queue item is executable (i.e., has started).

        Parameters
        ----------
        item_id : int
            The ID of the queue item.

        Returns
        -------
        bool
            True if the item is executable, False otherwise.
        """
        item = self.get_item_by_id(item_id)
        return item.buildable if item else False

    def remove_item_by_id(self, item_id: int) -> None:
        """
        Remove a specific QueueItem by its ID.

        Parameters
        ----------
        item_id : int
            The ID of the queue item to remove.
        """
        self.items = [item for item in self.items if item.id != item_id]
