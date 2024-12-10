import unittest
from app import app
from utils.db_utils import reset_test_database


class TestAuthRoutes(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client and reset the test database.
        """
        self.client = app.test_client()
        reset_test_database()

    def test_create_account(self):
        """
        Test the /auth/create-account endpoint.
        """
        response = self.client.post("/auth/create-account", json={
            "username": "testuser",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created successfully", response.get_json().get("message"))

    def test_login_success(self):
        """
        Test successful login for a user.
        """
        # First, create the account
        self.client.post("/auth/create-account", json={
            "username": "testuser",
            "password": "securepassword123"
        })

        # Then, attempt login
        response = self.client.post("/auth/login", json={
            "username": "testuser",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.get_json().get("message"))

    def test_login_failure(self):
        """
        Test failed login due to incorrect credentials.
        """
        # Attempt login without creating the user
        response = self.client.post("/auth/login", json={
            "username": "nonexistentuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid username or password", response.get_json().get("error"))


if __name__ == "__main__":
    unittest.main()