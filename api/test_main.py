import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app


class GameApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_preflight_allows_both_live_server_origins(self):
        for origin in ("http://127.0.0.1:5500", "http://localhost:5500"):
            with self.subTest(origin=origin):
                response = self.client.options(
                    "/fraseMaleida/v1/generate-game",
                    headers={
                        "Origin": origin,
                        "Access-Control-Request-Method": "POST",
                        "Access-Control-Request-Headers": "content-type",
                    },
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.headers["access-control-allow-origin"], origin)

    def test_preflight_rejects_other_origins(self):
        response = self.client.options(
            "/fraseMaleida/v1/generate-game",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "POST",
            },
        )
        self.assertEqual(response.status_code, 400)

    @patch("api.main.get_db_connection")
    def test_create_game_accepts_json_and_existing_query_parameter(self, connect):
        cursor = connect.return_value.cursor.return_value
        cursor.lastrowid = 42
        for request in ({"json": {"phrase": "hello"}}, {"params": {"phrase": "hello"}}):
            with self.subTest(request=request):
                response = self.client.post(
                    "/fraseMaleida/v1/generate-game",
                    headers={"Origin": "http://127.0.0.1:5500"},
                    **request,
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.headers["access-control-allow-origin"], "http://127.0.0.1:5500")
                self.assertEqual(response.json(), {"url": "http://127.0.0.1:8000/fraseMaleida/v1/game/42"})
                cursor.execute.assert_called_with("INSERT INTO games (phrase) VALUES (%s)", ("hello",))

    def test_create_game_requires_phrase(self):
        response = self.client.post("/fraseMaleida/v1/generate-game")
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
