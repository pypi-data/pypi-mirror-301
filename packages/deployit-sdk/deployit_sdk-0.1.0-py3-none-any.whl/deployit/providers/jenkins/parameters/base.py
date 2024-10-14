from typing import Dict


class DeployParameters:
    def __init__(self, **kwargs):
        """
        Initialize deploy parameters with the given environment.

        Parameters
        ----------
        environment : Environment
            The environment in which the deployment will occur.
        """
        self.params = kwargs

    def to_url_query(self) -> str:
        """
        Generalize the function to accept a dictionary of parameters.

        Returns
        -------
        str
            A string formatted as URL parameters.
        """
        param_strs = []
        for key, value in self.params.items():
            if isinstance(value, list):
                value = "%0D%0A".join(value)
            param_strs.append(f"name={key}&value={value}")
        return "&".join(param_strs)

    def to_dict(self) -> Dict[str, str]:
        """
        Convert deploy parameters to a dictionary.

        Returns
        -------
        dict
            A dictionary representing the deploy parameters.
        """
        return {**self.params}
