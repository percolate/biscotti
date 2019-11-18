import unittest
from unittest import mock

from jose import jwt

from app import app, SECRET_HEADER

ALL_UI_EXTENSIONS = (
    "/top_nav",
    "/campaign",
    "/content",
    "/asset",
    "/request",
    "/task",
    "/settings",
)
ALL_LIFECYCLE_EVENTS = (
    "/install",
    "/uninstall",
    "/enable",
    "/disable",
    "/update",
    "/upgrade",
)


class TestBiscotti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.secret = "a" * 64
        cls.secret_mock = mock.patch("app.get_app_secret", return_value=cls.secret)
        cls.secret_mock.start()
        cls.wrong_secret = "b" * 64

    def test_ui_extensions(self):
        token = jwt.encode({"banana": 42}, self.secret)
        for location in ALL_UI_EXTENSIONS:
            resp = self.app.get("{}?jwt={}".format(location, token))
            self.assertEqual(resp.status_code, 200)
            self.assertIn("banana", str(resp.data))

    def test_ui_extensions_wrong_jwt_secret(self):
        token = jwt.encode({"banana": 42}, self.wrong_secret)
        for location in ALL_UI_EXTENSIONS:
            resp = self.app.get("{}?jwt={}".format(location, token))
            self.assertEqual(resp.status_code, 200)
            self.assertIn("invalid jwt", str(resp.data))

    @mock.patch("app.print")
    def test_lifecycle_callbacks(self, mock_print):
        for event in ALL_LIFECYCLE_EVENTS:
            mock_print.reset_mock()
            resp = self.app.post(
                event, headers={SECRET_HEADER: self.secret}, json={"banana": 42}
            )
            self.assertEqual(resp.status_code, 200)
            self.assertIn("banana", str(resp.data))
            self.assertIn("banana", mock_print.mock_calls[0][1][0])

    @mock.patch("app.print")
    def test_lifecycle_callbacks_wrong_header_secret(self, mock_print):
        for event in ALL_LIFECYCLE_EVENTS:
            mock_print.reset_mock()
            resp = self.app.post(
                event,
                headers={"X-Perc-App-Secret": self.wrong_secret},
                json={"banana": 42},
            )
            self.assertEqual(resp.status_code, 200)
            self.assertIn("banana", str(resp.data))
            self.assertIn("WARNING", mock_print.mock_calls[0][1][0])


if __name__ == "__main__":
    unittest.main()
