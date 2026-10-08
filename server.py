import json
from http.server import BaseHTTPRequestHandler


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
