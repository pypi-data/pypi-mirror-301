import pytest

from deployit.providers.jenkins.utils.filter import get_value_by_path, matches_filter


@pytest.fixture
def sample_data():
    return {
        "name": "Project X",
        "version": "1.0.0",
        "details": {"owner": "John Doe", "status": "active"},
        "tags": ["python", "web", "api"],
        "builds": [
            {"id": 1, "status": "success"},
            {"id": 2, "status": "failure"},
            {"id": 3, "status": "success"},
        ],
    }


def test_get_value_by_path_simple(sample_data):
    assert get_value_by_path(sample_data, "name") == "Project X"
    assert get_value_by_path(sample_data, "version") == "1.0.0"


def test_get_value_by_path_nested(sample_data):
    assert get_value_by_path(sample_data, "details.owner") == "John Doe"
    assert get_value_by_path(sample_data, "details.status") == "active"


def test_get_value_by_path_list(sample_data):
    assert get_value_by_path(sample_data, "tags") == ["python", "web", "api"]
    assert get_value_by_path(sample_data, "builds.id") == [1, 2, 3]
    assert get_value_by_path(sample_data, "builds.status") == [
        "success",
        "failure",
        "success",
    ]


def test_get_value_by_path_nonexistent():
    data = {"a": {"b": "c"}}
    assert get_value_by_path(data, "a.b.c") is None
    assert get_value_by_path(data, "x.y.z") is None


def test_get_value_by_path_empty_path():
    data = {"a": "b"}
    assert get_value_by_path(data, "") == data


def test_matches_filter_simple(sample_data):
    assert matches_filter(sample_data, {"name": "Project X"})
    assert matches_filter(sample_data, {"version": "1.0.0"})
    assert not matches_filter(sample_data, {"name": "Project Y"})


def test_matches_filter_nested(sample_data):
    assert matches_filter(sample_data, {"details.owner": "John Doe"})
    assert matches_filter(sample_data, {"details.status": "active"})
    assert not matches_filter(sample_data, {"details.owner": "Jane Doe"})


def test_matches_filter_list(sample_data):
    assert matches_filter(sample_data, {"tags": "python"})
    assert matches_filter(sample_data, {"tags": "web"})
    assert not matches_filter(sample_data, {"tags": "java"})


def test_matches_filter_multiple_conditions(sample_data):
    assert matches_filter(
        sample_data, {"name": "Project X", "details.status": "active", "tags": "web"}
    )
    assert not matches_filter(
        sample_data, {"name": "Project X", "details.status": "inactive", "tags": "web"}
    )


def test_matches_filter_empty():
    assert matches_filter({}, {})
    assert matches_filter({"a": "b"}, {})


def test_matches_filter_nonexistent_path(sample_data):
    assert not matches_filter(sample_data, {"nonexistent.path": "value"})


def test_get_value_by_path_nested_list():
    data = {"a": [{"b": 1}, {"b": 2}]}
    assert get_value_by_path(data, "a.b") == [1, 2]


def test_matches_filter_nested_list():
    data = {"a": [{"b": 1}, {"b": 2}]}
    assert matches_filter(data, {"a.b": 1})
    assert matches_filter(data, {"a.b": 2})
    assert not matches_filter(data, {"a.b": 3})


def test_get_value_by_path_list_of_lists():
    data = {"a": [[1, 2], [3, 4]]}
    assert get_value_by_path(data, "a") == [[1, 2], [3, 4]]


def test_matches_filter_list_of_lists():
    data = {"a": [[1, 2], [3, 4]]}
    assert matches_filter(data, {"a": [1, 2]})
    assert matches_filter(data, {"a": [3, 4]})
    assert not matches_filter(data, {"a": [5, 6]})
