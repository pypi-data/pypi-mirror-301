from typing import Any

from deployit.providers.jenkins.clients.http import RequestsHTTPClient
from deployit.providers.jenkins.models.url import JenkinsURLBuilder


class JenkinsAPIClient:
    def __init__(self, url_builder: JenkinsURLBuilder, http_client: RequestsHTTPClient):
        """
        Initialize the JenkinsAPIClient with a URL builder and HTTP client.

        Parameters
        ----------
        url_builder : JenkinsURLBuilder
            The URL builder instance.
        http_client : HTTPClient
            The HTTP client instance.
        """
        self.url_builder = url_builder
        self.http_client = http_client

    def make_request(
        self, endpoint_template: str, method: str = "GET", is_json=True, **kwargs
    ) -> Any:
        """
        Make a request to the Jenkins API.

        Parameters
        ----------
        endpoint_template : str
            The template of the endpoint URL.
        method : str, optional
            The HTTP method to use (default is 'GET').
        kwargs : dict
            Additional parameters to format the endpoint template.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        ValueError
            If an unsupported method is used.
        """
        headers = kwargs.get("headers", {})
        url = self.url_builder.build_url(
            endpoint_template,
            **{
                k: v
                for k, v in kwargs.items()
                if k not in ["headers", "data", "is_json"]
            },
        )
        if method == "GET":
            return self.http_client.get(url, headers=headers, is_json=is_json)
        if method == "POST":
            return self.http_client.post(
                url, headers=headers, data=kwargs.get("data"), is_json=is_json
            )
        if method == "PUT":
            return self.http_client.put(
                url, headers=headers, data=kwargs.get("data"), is_json=is_json
            )
        if method == "DELETE":
            return self.http_client.delete(url, headers=headers, is_json=is_json)
        raise ValueError(f"Unsupported method: {method}")
