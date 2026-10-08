import uuid

def test_get_users_returns_success_status(users_api):
    response = users_api.get_users()

    assert response.status_code == 200


def test_get_users_returns_list_of_users(users_api):
    response = users_api.get_users()
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["data"]

    assert len(response_body["data"]) == 2
    assert response_body["data"][0]["name"] == "Ivan"


def test_get_existing_user(users_api, user_for_test):
    response = users_api.get_user(user_for_test["id"])
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["data"]["id"] == user_for_test["id"]
    assert response_body["data"]["job"] == user_for_test["job"]
    assert response_body["data"]["name"] == user_for_test["name"]


def test_get_created_user(users_api, user_for_test):
    response = users_api.get_user(user_for_test["id"])
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["data"] == user_for_test


def test_get_missing_user_returns_not_found(users_api):
    response = users_api.get_user(999)
    response_body = response.json()

    assert response.status_code == 404
    assert response_body["error"] == "User not found"

def test_change_data_user(users_api, user_for_test):
    response = users_api.get_user(user_for_test["id"]).json()
    name = response["data"]["name"]
    job = response["data"]["job"]
    new_name = uuid.uuid4().hex[:8]
    new_job = uuid.uuid4().hex[:8]
    print(response)
    change_data_response = users_api.post_user(user_for_test["id"], name=new_name, job=new_job)
    response_after_change_data = users_api.get_user(user_for_test["id"]).json()
    print(response_after_change_data)
    assert change_data_response.status_code == 200
    assert response_after_change_data["data"]["name"] == new_name
    assert response_after_change_data["data"]["name"] != name
    assert response_after_change_data["data"]["job"] == new_job
    assert response_after_change_data["data"]["job"] != job
