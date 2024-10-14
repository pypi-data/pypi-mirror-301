import pytest

from deployit.providers.jenkins.utils.decorators import make_singleton


def test_make_singleton_creates_single_instance():
    @make_singleton
    class TestClass:
        def __init__(self):
            self.value = 0

    instance1 = TestClass()
    instance2 = TestClass()

    assert instance1 is instance2
    assert id(instance1) == id(instance2)
    assert instance1.value == instance2.value == 0


def test_make_singleton_preserves_state():
    @make_singleton
    class TestClass:
        def __init__(self):
            self.value = 0

        def increment(self):
            self.value += 1

    instance1 = TestClass()
    instance1.increment()

    instance2 = TestClass()
    assert instance2.value == 1
    assert id(instance1) == id(instance2)


def test_make_singleton_with_arguments():
    @make_singleton
    class TestClass:
        def __init__(self, initial_value=0):
            self.value = initial_value

    instance1 = TestClass(5)
    instance2 = TestClass(10)  # This argument is ignored

    assert instance1 is instance2
    assert id(instance1) == id(instance2)
    assert instance1.value == instance2.value == 5


def test_make_singleton_with_multiple_classes():
    @make_singleton
    class ClassA:
        pass

    @make_singleton
    class ClassB:
        pass

    instance_a1 = ClassA()
    instance_a2 = ClassA()
    instance_b1 = ClassB()
    instance_b2 = ClassB()

    assert instance_a1 is instance_a2
    assert id(instance_a1) == id(instance_a2)
    assert instance_b1 is instance_b2
    assert id(instance_b1) == id(instance_b2)
    assert instance_a1 is not instance_b1
    assert id(instance_a1) != id(instance_b1)


def test_make_singleton_preserves_class_methods():
    @make_singleton
    class TestClass:
        @classmethod
        def class_method(cls):
            return "class method"

        @staticmethod
        def static_method():
            return "static method"

    instance = TestClass()
    assert instance.class_method() == "class method"
    assert instance.static_method() == "static method"
    assert TestClass().class_method() == "class method"
    assert TestClass().static_method() == "static method"


def test_make_singleton_with_properties():
    @make_singleton
    class TestClass:
        def __init__(self):
            self._value = 0

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, new_value):
            self._value = new_value

    instance1 = TestClass()
    instance1.value = 5

    instance2 = TestClass()
    assert instance2.value == 5
    assert id(instance1) == id(instance2)
