class QueueEndpoints:
    """
    Endpoints related to the Jenkins queue for a specific job.

    Attributes
    ----------
    QUEUE_INFO : str
        URL template to get information about the queue for a specific job.
    QUEUE_ITEM : str
        URL template to get information about a specific item in the queue for a specific job.
    CANCEL_QUEUE : str
        URL template to cancel a specific item in the queue for a specific job.
    """

    QUEUE_INFO: str = "/queue/api/json?depth=0"
    QUEUE_ITEM: str = "/queue/item/{number}/api/json?depth=1"
    CANCEL_QUEUE: str = "/queue/cancelItem?id={id}"
