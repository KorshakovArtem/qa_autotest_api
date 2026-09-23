import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from api_clients.base_client import BaseApiClient
from pages.users_api import UsersApi


class TestApiHandler(BaseHTTPRequestHandler):
    users = [
        {"id": 1, "name": "Ivan", "job": "QA Engineer"},
        {"id": 2, "name": "Anna", "job": "Developer"},
    ]

    def do_GET(self):
        if self.path == "/users":
            self._send_json(200, {"data": self.users})
            return

        if self.path.startswith("/users/"):
            user_id = int(self.path.split("/")[-1])
            user = next((item for item in self.users if item["id"] == user_id), None)

            if user is None:
                self._send_json(404, {"error": "User not found"})
                return

            self._send_json(200, {"data": user})
            return

        self._send_json(404, {"error": "Route not found"})

    def do_POST(self):
        if self.path != "/users":
            self._send_json(404, {"error": "Route not found"})
            return

        request_body = self.rfile.read(int(self.headers["Content-Length"]))
        payload = json.loads(request_body)

        created_user = {
            "id": 3,
            "name": payload["name"],
            "job": payload["job"],
        }

        self._send_json(201, {"data": created_user})

    def log_message(self, format, *args):
        return

    def _send_json(self, status_code, body):
        response = json.dumps(body).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


@pytest.fixture(scope="session")
def api_server_url():
    server = HTTPServer(("localhost", 0), TestApiHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    yield f"http://localhost:{server.server_port}"

    server.shutdown()
    thread.join()


@pytest.fixture
def api_client(api_server_url):
    return BaseApiClient(api_server_url)


@pytest.fixture
def users_api(api_client):
    return UsersApi(api_client)

