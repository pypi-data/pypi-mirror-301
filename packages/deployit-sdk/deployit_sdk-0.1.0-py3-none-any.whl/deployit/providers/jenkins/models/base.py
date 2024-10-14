class JenkinsObject:
    """
    Base class for all Jenkins objects.
    """

    def __str__(self):
        """
        Convert the object to a string.

        Returns
        -------
        str
            The string representation of the object.
        """
        return str(self.__dict__)

    def to_dict(self):
        """
        Convert the object to a dictionary.

        Returns
        -------
        dict
            The dictionary representation of the object.
        """
        return vars(self)
