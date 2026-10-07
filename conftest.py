import json
import threading
import uuid
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
            "id": max(user["id"] for user in self.users) + 1,
            "name": payload["name"],
            "job": payload["job"],
        }

        self.users.append(created_user)
        self._send_json(201, {"data": created_user})

    def do_DELETE(self):
        if self.path.startswith("/users/"):
            user_id = int(self.path.split("/")[-1])

            user = next((item for item in self.users if item["id"] == user_id), None)

            if user is None:
                self._send_json(404, {"error": "User not found"})
                return

            self.users.remove(user)
            self._send_json(204, {})
            return

        self._send_json(404, {"error": "Route not found"})


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


@pytest.fixture
def create_random_user(users_api):
    def _create_random_user():
        response = users_api.create_user(
            name=f"user_{uuid.uuid4().hex[:8]}",
            job=f"job_{uuid.uuid4().hex[:8]}",
        )
        return response

    return _create_random_user


@pytest.fixture
def create_user(users_api):
    def _create_user(name, job):
        response = users_api.create_user(name, job)
        return response.json()["data"]
    return _create_user

@pytest.fixture
def delete_user(users_api):
    def _delete_user(user_id):
        return users_api.delete_user(user_id)

    return _delete_user


@pytest.fixture
def user_for_test(create_random_user, delete_user):
    create_response = create_random_user()
    user = create_response.json()["data"]

    yield user

    delete_user(user["id"])
