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
