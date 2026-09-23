def test_get_users_returns_success_status(users_api):
    response = users_api.get_users()

    assert response.status_code == 200


def test_get_users_returns_list_of_users(users_api):
    response = users_api.get_users()
    response_body = response.json()

    assert len(response_body["data"]) == 2
    assert response_body["data"][0]["name"] == "Ivan"


def test_get_existing_user(users_api):
    response = users_api.get_user(1)
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["data"]["id"] == 1
    assert response_body["data"]["job"] == "QA Engineer"


def test_create_user(users_api):
    response = users_api.create_user(name="Petr", job="QA Automation")
    response_body = response.json()

    assert response.status_code == 201
    assert response_body["data"]["name"] == "Petr"
    assert response_body["data"]["job"] == "QA Automation"


def test_get_missing_user_returns_not_found(users_api):
    response = users_api.get_user(999)
    response_body = response.json()

    assert response.status_code == 404
    assert response_body["error"] == "User not found"
