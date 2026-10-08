import threading
from http.server import HTTPServer
import uuid

import pytest

from api_clients.base_client import BaseApiClient
from pages.users_api import UsersApi
from server import TestApiHandler


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
        return users_api.create_user(
            name=f"user_{uuid.uuid4().hex[:8]}",
            job=f"job_{uuid.uuid4().hex[:8]}",
        )

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
