class UsersApi:
    def __init__(self, client):
        self.client = client

    def get_users(self):
        return self.client.get("/users")

    def get_user(self, user_id):
        return self.client.get(f"/users/{user_id}")

    def create_user(self, name, job):
        payload = {
            "name": name,
            "job": job,
        }
        return self.client.post("/users", json=payload)

