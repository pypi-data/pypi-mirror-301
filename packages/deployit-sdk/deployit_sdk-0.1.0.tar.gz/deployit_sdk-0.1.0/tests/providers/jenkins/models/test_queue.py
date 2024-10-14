import pytest

from deployit.providers.jenkins.models.queue import Queue, QueueItem


@pytest.fixture
def sample_queue_info():
    return {
        "items": [
            {
                "id": 1,
                "task": {"name": "Job1", "url": "http://jenkins.example.com/job/Job1/"},
                "buildable": True,
                "params": {"PARAM1": "VALUE1"},
                "why": "Waiting for next available executor",
            },
            {
                "id": 2,
                "task": {"name": "Job2", "url": "http://jenkins.example.com/job/Job2/"},
                "buildable": False,
                "why": "Build #1 is already in progress",
            },
            {
                "id": 3,
                "task": {"name": "Job3", "url": "http://jenkins.example.com/job/Job3/"},
                "buildable": True,
                "executable": {"number": 5},
            },
        ]
    }


def test_queue_initialization(sample_queue_info):
    queue = Queue(sample_queue_info)
    assert len(queue.items) == 3
    assert all(isinstance(item, QueueItem) for item in queue.items)


def test_queue_item_attributes(sample_queue_info):
    queue = Queue(sample_queue_info)

    item1 = queue.items[0]
    assert item1.id == 1
    assert item1.task_name == "Job1"
    assert item1.url == "http://jenkins.example.com/job/Job1/"
    assert item1.buildable == True
    assert item1.params == {"PARAM1": "VALUE1"}
    assert item1.why == "Waiting for next available executor"
    assert item1.build_id is None

    item2 = queue.items[1]
    assert item2.id == 2
    assert item2.task_name == "Job2"
    assert item2.url == "http://jenkins.example.com/job/Job2/"
    assert item2.buildable == False
    assert item2.params is None
    assert item2.why == "Build #1 is already in progress"
    assert item2.build_id is None

    item3 = queue.items[2]
    assert item3.id == 3
    assert item3.task_name == "Job3"
    assert item3.url == "http://jenkins.example.com/job/Job3/"
    assert item3.buildable == True
    assert item3.params is None
    assert item3.why is None
    assert item3.build_id == 5


def test_get_item_by_id(sample_queue_info):
    queue = Queue(sample_queue_info)

    item = queue.get_item_by_id(2)
    assert item is not None
    assert item.id == 2
    assert item.task_name == "Job2"

    non_existent_item = queue.get_item_by_id(999)
    assert non_existent_item is None


def test_is_item_executable(sample_queue_info):
    queue = Queue(sample_queue_info)

    assert queue.is_item_executable(1) == True
    assert queue.is_item_executable(2) == False
    assert queue.is_item_executable(3) == True
    assert queue.is_item_executable(999) == False


def test_remove_item_by_id(sample_queue_info):
    queue = Queue(sample_queue_info)

    assert len(queue.items) == 3
    queue.remove_item_by_id(2)
    assert len(queue.items) == 2
    assert all(item.id != 2 for item in queue.items)

    # Removing non-existent item should not raise an error
    queue.remove_item_by_id(999)
    assert len(queue.items) == 2


def test_queue_with_empty_info():
    empty_queue_info = {"items": []}
    queue = Queue(empty_queue_info)
    assert len(queue.items) == 0


def test_queue_with_missing_fields():
    incomplete_queue_info = {
        "items": [
            {
                "id": 1,
                "task": {
                    "name": "IncompleteJob",
                    "url": "http://jenkins.example.com/job/IncompleteJob/",
                },
            }
        ]
    }
    queue = Queue(incomplete_queue_info)
    assert len(queue.items) == 1
    item = queue.items[0]
    assert item.id == 1
    assert item.task_name == "IncompleteJob"
    assert item.url == "http://jenkins.example.com/job/IncompleteJob/"
    assert item.buildable == False
    assert item.params is None
    assert item.why is None
    assert item.build_id is None


def test_queue_item_dataclass():
    item = QueueItem(
        id=1,
        task_name="TestJob",
        url="http://jenkins.example.com/job/TestJob/",
        buildable=True,
        params={"PARAM": "VALUE"},
        why="Waiting",
        build_id=10,
    )
    assert item.id == 1
    assert item.task_name == "TestJob"
    assert item.url == "http://jenkins.example.com/job/TestJob/"
    assert item.buildable == True
    assert item.params == {"PARAM": "VALUE"}
    assert item.why == "Waiting"
    assert item.build_id == 10
