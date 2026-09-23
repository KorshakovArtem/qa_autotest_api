from urllib.parse import urljoin

import requests


class BaseApiClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/") + "/"
        self.session = requests.Session()

    def get(self, path, **kwargs):
        return self.session.get(self._url(path), **kwargs)

    def post(self, path, **kwargs):
        return self.session.post(self._url(path), **kwargs)

    def _url(self, path):
        return urljoin(self.base_url, path.lstrip("/"))

