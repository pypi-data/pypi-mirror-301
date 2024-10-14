from unittest.mock import Mock, patch

import pytest

from deployit.providers.jenkins.clients.jenkins import JenkinsAPIClient
from deployit.providers.jenkins.endpoints.queue import QueueEndpoints
from deployit.providers.jenkins.models.queue import Queue, QueueItem
from deployit.providers.jenkins.services.queue import QueueApiService


@pytest.fixture
def mock_jenkins_client():
    return Mock(spec=JenkinsAPIClient)


@pytest.fixture
def queue_service(mock_jenkins_client):
    return QueueApiService(mock_jenkins_client)


def test_queue_api_service_initialization(queue_service, mock_jenkins_client):
    assert isinstance(queue_service, QueueApiService)
    assert queue_service.jenkins_client == mock_jenkins_client


def test_get_queue(queue_service, mock_jenkins_client):
    mock_queue_info = {
        "items": [
            {
                "id": 1,
                "task": {"name": "Job1", "url": "http://jenkins.example.com/job/Job1"},
            },
            {
                "id": 2,
                "task": {"name": "Job2", "url": "http://jenkins.example.com/job/Job2"},
            },
        ]
    }
    mock_jenkins_client.make_request.return_value = mock_queue_info

    result = queue_service.get_queue()

    assert isinstance(result, Queue)
    assert len(result.items) == 2
    mock_jenkins_client.make_request.assert_called_once_with(
        QueueEndpoints.QUEUE_INFO, method="GET"
    )


def test_get_queue_item(queue_service, mock_jenkins_client):
    mock_queue_item_info = {
        "id": 1,
        "task": {"name": "Job1", "url": "http://jenkins.example.com/job/Job1"},
        "buildable": True,
        "params": {"param1": "value1"},
        "why": "Waiting for next available executor",
        "executable": {"number": 5},
    }
    mock_jenkins_client.make_request.return_value = mock_queue_item_info

    result = queue_service.get_queue_item(1)

    assert isinstance(result, QueueItem)
    assert result.id == 1
    assert result.task_name == "Job1"
    assert result.url == "http://jenkins.example.com/job/Job1"
    assert result.buildable == True
    assert result.params == {"param1": "value1"}
    assert result.why == "Waiting for next available executor"
    assert result.build_id == 5
    mock_jenkins_client.make_request.assert_called_once_with(
        QueueEndpoints.QUEUE_ITEM, method="GET", number=1
    )


def test_get_queue_item_missing_fields(queue_service, mock_jenkins_client):
    mock_queue_item_info = {
        "id": 1,
        "task": {"name": "Job1", "url": "http://jenkins.example.com/job/Job1"},
    }
    mock_jenkins_client.make_request.return_value = mock_queue_item_info

    result = queue_service.get_queue_item(1)

    assert isinstance(result, QueueItem)
    assert result.id == 1
    assert result.task_name == "Job1"
    assert result.url == "http://jenkins.example.com/job/Job1"
    assert result.buildable == False
    assert result.params is None
    assert result.why is None
    assert result.build_id is None


def test_cancel_queue_item(queue_service, mock_jenkins_client):
    mock_response = {"cancelled": True}
    mock_jenkins_client.make_request.return_value = mock_response

    result = queue_service.cancel_queue_item(1)

    assert result == mock_response
    mock_jenkins_client.make_request.assert_called_once_with(
        QueueEndpoints.CANCEL_QUEUE, method="POST", id=1
    )


@pytest.mark.parametrize(
    "method_name, endpoint, expected_args, mock_return",
    [
        ("get_queue", QueueEndpoints.QUEUE_INFO, {}, {"items": []}),
        (
            "get_queue_item",
            QueueEndpoints.QUEUE_ITEM,
            {"number": 1},
            {"id": 1, "task": {"name": "Job1", "url": "http://example.com"}},
        ),
        ("cancel_queue_item", QueueEndpoints.CANCEL_QUEUE, {"id": 1}, {}),
    ],
)
def test_api_methods_use_correct_endpoints(
    queue_service,
    mock_jenkins_client,
    method_name,
    endpoint,
    expected_args,
    mock_return,
):
    mock_jenkins_client.make_request.return_value = mock_return
    method = getattr(queue_service, method_name)

    if method_name == "get_queue":
        result = method()
    else:
        result = method(1)

    mock_jenkins_client.make_request.assert_called_once_with(
        endpoint,
        method="GET" if method_name.startswith("get") else "POST",
        **expected_args,
    )

    if method_name == "get_queue":
        assert isinstance(result, Queue)
    elif method_name == "get_queue_item":
        assert isinstance(result, QueueItem)
    else:
        assert result == mock_return
