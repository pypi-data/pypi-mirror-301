def make_singleton(cls):
    """
    Decorator to make a class a singleton.

    Ensures that only one instance of the class is created. If an instance
    already exists, it returns the existing instance.

    Parameters
    ----------
    cls : type
        The class to be decorated as a singleton.

    Returns
    -------
    instance : function
        A function that returns the singleton instance of the class.

    Examples
    --------
    >>> @singleton
    ... class MyClass:
    ...     pass
    ...
    >>> obj1 = MyClass()
    >>> obj2 = MyClass()
    >>> obj1 is obj2
    True
    """
    instances = {}
    initialized = {}

    # Using a wrapper class to preserve the ability to inherit
    class SingletonWrapper(cls):
        def __new__(cls, *args, **kwargs):
            if cls not in instances:
                instances[cls] = super(SingletonWrapper, cls).__new__(cls)
                initialized[cls] = False
            return instances[cls]

        def __init__(self, *args, **kwargs):
            # Ensure __init__ is called only once
            if not initialized[self.__class__]:
                super(SingletonWrapper, self).__init__(*args, **kwargs)
                initialized[self.__class__] = True

    return SingletonWrapper
