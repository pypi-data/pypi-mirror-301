import pytest

from deployit.providers.jenkins.models.base import JenkinsObject


class TestJenkinsObject:
    @pytest.fixture
    def jenkins_object(self):
        return JenkinsObject()

    def test_jenkins_object_initialization(self, jenkins_object):
        assert isinstance(jenkins_object, JenkinsObject)

    def test_str_representation(self, jenkins_object):
        assert str(jenkins_object) == "{}"

    def test_to_dict_empty_object(self, jenkins_object):
        assert jenkins_object.to_dict() == {}

    def test_str_representation_with_attributes(self):
        class CustomJenkinsObject(JenkinsObject):
            def __init__(self):
                self.attr1 = "value1"
                self.attr2 = 42

        custom_obj = CustomJenkinsObject()
        expected_str = "{'attr1': 'value1', 'attr2': 42}"
        assert str(custom_obj) == expected_str

    def test_to_dict_with_attributes(self):
        class CustomJenkinsObject(JenkinsObject):
            def __init__(self):
                self.attr1 = "value1"
                self.attr2 = 42

        custom_obj = CustomJenkinsObject()
        expected_dict = {"attr1": "value1", "attr2": 42}
        assert custom_obj.to_dict() == expected_dict

    def test_str_representation_with_nested_object(self):
        class NestedObject:
            def __init__(self):
                self.nested_attr = "nested_value"

        class CustomJenkinsObject(JenkinsObject):
            def __init__(self):
                self.attr1 = "value1"
                self.nested = NestedObject()

        custom_obj = CustomJenkinsObject()
        result_str = str(custom_obj)

        assert "'attr1': 'value1'" in result_str
        assert "'nested': <" in result_str
        assert "NestedObject object at" in result_str

    def test_to_dict_with_nested_object(self):
        class NestedObject:
            def __init__(self):
                self.nested_attr = "nested_value"

        class CustomJenkinsObject(JenkinsObject):
            def __init__(self):
                self.attr1 = "value1"
                self.nested = NestedObject()

        custom_obj = CustomJenkinsObject()
        result_dict = custom_obj.to_dict()

        assert result_dict["attr1"] == "value1"
        assert isinstance(result_dict["nested"], NestedObject)
        assert hasattr(result_dict["nested"], "nested_attr")
        assert result_dict["nested"].nested_attr == "nested_value"

    def test_str_representation_with_complex_types(self):
        class CustomJenkinsObject(JenkinsObject):
            def __init__(self):
                self.list_attr = [1, 2, 3]
                self.dict_attr = {"key": "value"}
                self.tuple_attr = (4, 5, 6)

        custom_obj = CustomJenkinsObject()
        expected_str = "{'list_attr': [1, 2, 3], 'dict_attr': {'key': 'value'}, 'tuple_attr': (4, 5, 6)}"
        assert str(custom_obj) == expected_str

    def test_to_dict_with_complex_types(self):
        class CustomJenkinsObject(JenkinsObject):
            def __init__(self):
                self.list_attr = [1, 2, 3]
                self.dict_attr = {"key": "value"}
                self.tuple_attr = (4, 5, 6)

        custom_obj = CustomJenkinsObject()
        expected_dict = {
            "list_attr": [1, 2, 3],
            "dict_attr": {"key": "value"},
            "tuple_attr": (4, 5, 6),
        }
        assert custom_obj.to_dict() == expected_dict
