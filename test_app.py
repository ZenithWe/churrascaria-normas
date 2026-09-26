import os
import tempfile
import unittest

os.environ.setdefault("ADMIN_PASSWORD", "test-password")

import app as normas_app


class SiteTest(unittest.TestCase):
    def setUp(self):
        normas_app.app.config.update(TESTING=True, SECRET_KEY="test")
        self.client = normas_app.app.test_client()

    def test_home(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Norma", res.data)

    def test_health(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["status"], "ok")

    def test_admin_requires_login(self):
        res = self.client.get("/admin")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/admin/login", res.location)


if __name__ == "__main__":
    unittest.main()
