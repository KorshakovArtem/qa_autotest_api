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

    def delete_user(self, user_id):
        return self.client.delete(f"/users/{user_id}")

    def post_user(self, user_id, **fields):
        payload = fields
        return self.client.post(f"/users/{user_id}", json=payload)
