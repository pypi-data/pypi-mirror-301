import base64
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import requests

from deployit.providers.jenkins.endpoints.common import COMMON_HEADERS, CommonEndpoints
from deployit.providers.jenkins.utils.config import Config
from deployit.providers.jenkins.utils.errors import JenkinsConnectionError


class HTTPClient(ABC):
    @abstractmethod
    def get(self, url: str, headers: Optional[Dict[str, str]] = {}) -> Dict:
        """
        Send a GET request.

        Parameters
        ----------
        url : str
            The URL to send the GET request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        dict
            The response JSON.
        """

    @abstractmethod
    def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = {},
        data: Optional[Dict[str, str]] = {},
    ) -> Dict:
        """
        Send a POST request.

        Parameters
        ----------
        url : str
            The URL to send the POST request to.
        headers : dict, optional
            Optional headers to include in the request.
        data : dict, optional
            Data to include in the POST request.

        Returns
        -------
        dict
            The response JSON.
        """

    @abstractmethod
    def delete(self, url: str, headers: Optional[Dict[str, str]] = {}) -> Dict:
        """
        Send a DELETE request.

        Parameters
        ----------
        url : str
            The URL to send the DELETE request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        dict
            The response JSON.
        """

    @abstractmethod
    def put(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = {},
        data: Optional[Dict[str, str]] = {},
    ) -> Dict:
        """
        Send a PUT request.

        Parameters
        ----------
        url : str
            The URL to send the PUT request to.
        headers : dict, optional
            Optional headers to include in the request.
        data : dict, optional
            Data to include in the PUT request.

        Returns
        -------
        dict
            The response JSON.
        """


class RequestsHTTPClient(HTTPClient):
    def __init__(self):
        self._set_base_header()

    def _set_base_header(self):
        credentials = f"{Config.USERNAME}:{Config.API_TOKEN}"
        base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )
        auth_header = {"Authorization": f"Basic {base64_credentials}"}
        try:
            response = requests.get(
                f"{Config.JENKINS_DOMAIN}/{CommonEndpoints.CRUMB_ISSUER}",
                headers=auth_header,
                verify=False,
            ).json()
            self._base_header = {
                **COMMON_HEADERS,
                **auth_header,
                **{response.get("crumbRequestField"): response.get("crumb")},
            }
        except requests.exceptions.RequestException as e:
            print(
                f"An error occurred, verify your environment variables if they are setted correctly: {e}"
            )

    def _process_response(
        self, response: requests.Response, is_json: bool
    ) -> Dict[Any, Any]:
        """
        Process the response based on the is_json flag.

        Parameters
        ----------
        response : requests.Response
            The response object from the request.
        is_json : bool
            Whether to parse the response as JSON.

        Returns
        -------
        dict
            The processed response data.
        """
        if is_json:
            try:
                return response.json()
            except ValueError:
                return {"content": response._content}
        return {"content": response.text}

    def get(
        self, url: str, headers: Optional[Dict[str, str]] = None, is_json: bool = True
    ) -> Dict[Any, Any]:
        """
        Send a GET request using the requests library.

        Parameters
        ----------
        url : str
            The URL to send the GET request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        JenkinsError
            If the GET request fails.
        """
        headers = {**self._base_header, **(headers or {})}
        try:
            response = requests.get(url, headers=headers, timeout=Config.TIMEOUT)
            response.raise_for_status()
            if is_json:
                try:
                    return response.json()
                except ValueError:
                    return {"content": response._content}
            if response._content and hasattr(response._content, "decode"):
                return {"content": response._content.decode("utf-8")}
            return {"content": response.text}
        except (ValueError, requests.exceptions.RequestException) as e:
            raise JenkinsConnectionError(f"GET request failed: {str(e)}") from e

    def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict] = None,
        is_json: bool = True,
    ) -> Dict:
        """
        Send a POST request using the requests library.

        Parameters
        ----------
        url : str
            The URL to send the POST request to.
        headers : dict, optional
            Optional headers to include in the request.
        data : dict, optional
            Data to include in the POST request.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        JenkinsError
            If the POST request fails.
        """
        headers = {**self._base_header, **(headers or {})}
        try:
            response = requests.post(
                url, headers=headers, data=data, timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            if (
                hasattr(response, "json")
                and response.status_code != 204
                and response.content != b""
            ):
                return response.json()
            return {
                **response.headers,
                "content": response.content,
                "text": response.text,
            }
        except requests.exceptions.RequestException as e:
            raise JenkinsConnectionError(f"POST request failed: {e}")

    def delete(
        self, url: str, headers: Optional[Dict[str, str]] = {}, is_json: bool = True
    ) -> Dict:
        """
        Send a DELETE request using the requests library.

        Parameters
        ----------
        url : str
            The URL to send the DELETE request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        JenkinsError
            If the DELETE request fails.
        """
        headers = {**self._base_header, **(headers or {})}
        try:
            response = requests.delete(url, headers=headers, timeout=Config.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise JenkinsConnectionError(f"DELETE request failed: {e}")

    def put(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = {},
        data: Optional[Dict[str, str]] = {},
        is_json: bool = True,
    ) -> Dict:
        """
        Send a PUT request using the requests library.

        Parameters
        ----------
        url : str
            The URL to send the PUT request to.
        headers : dict, optional
            Optional headers to include in the request.
        data : dict, optional
            Data to include in the PUT request.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        JenkinsError
            If the PUT request fails.
        """
        headers = {**self._base_header, **(headers or {})}
        try:
            response = requests.put(
                url, headers=headers, data=data, timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise JenkinsConnectionError(f"PUT request failed: {e}")
