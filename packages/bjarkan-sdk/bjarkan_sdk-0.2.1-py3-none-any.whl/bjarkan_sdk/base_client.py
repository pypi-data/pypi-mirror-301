import requests
from .exceptions import BjarkanClientError


class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None

    def authenticate(self, username: str, password: str):
        response = requests.post(f"{self.base_url}/token", data={"username": username, "password": password})
        response.raise_for_status()
        self.token = response.json()["access_token"]

    def _get_headers(self):
        if not self.token:
            raise ValueError("You must authenticate before making requests")
        return {"Authorization": f"Bearer {self.token}"}

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise BjarkanClientError(f"Client error: {e.response.json().get('detail', str(e))}")
            elif e.response.status_code == 403:
                raise BjarkanClientError("Authentication failed or insufficient permissions")
            elif e.response.status_code == 500:
                raise BjarkanClientError("Server error occurred. Please try again later.")
            else:
                raise BjarkanClientError(f"HTTP error occurred: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise BjarkanClientError(f"Error sending request: {str(e)}")