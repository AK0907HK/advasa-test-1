from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class CoreTests(APITestCase):
    def signup(self, username="u", password="pw", allowance=5000):
        res = self.client.post("/api/users/", {
            "username": username, "password": password, "initial_allowance": allowance
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def login(self, username="u", password="pw"):
        res = self.client.post("/api/auth/token/", {
            "username": username, "password": password
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        access = res.data["access"]
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        return c

    def setUp(self):
        self.signup("alice", "pass", allowance=5000)
        self.c = self.login("alice", "pass")

    def test_me_returns_available_amount(self):
        res = self.c.get("/api/me/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("available_amount", res.data)

    def test_apply_success_decrements_balance(self):
        res = self.c.post("/api/applications/", {"amount": 1000}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        me = self.c.get("/api/me/")
        self.assertEqual(me.status_code, status.HTTP_200_OK)
        self.assertEqual(me.data["available_amount"], 4000)

    def test_apply_insufficient_returns_400(self):
        res = self.c.post("/api/applications/", {"amount": 999999}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
