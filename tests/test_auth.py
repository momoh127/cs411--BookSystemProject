import unittest
import bcrypt
from utils.auth_utils import hash_password, verify_password 
class TestPasswordUtils(unittest.TestCase):

    def test_hash_password(self):
        """
        Test that the `hash_password` function returns a valid bcrypt hash.
        """
        password = "mypassword"
        hashed_password = hash_password(password)

        # Check that the hashed password is a valid bcrypt hash
        self.assertTrue(hashed_password.startswith("$2b$"))  # Bcrypt hashes start with "$2b$" or similar
        self.assertGreater(len(hashed_password), 0)

    def test_verify_password_correct(self):
        """
        Test that `verify_password` returns True for a correct password.
        """
        password = "mypassword"
        hashed_password = hash_password(password)

        # Verify the password
        self.assertTrue(verify_password(password, hashed_password))

    def test_verify_password_incorrect(self):
        """
        Test that `verify_password` returns False for an incorrect password.
        """
        password = "mypassword"
        wrong_password = "wrongpassword"
        hashed_password = hash_password(password)

        # Verify the wrong password
        self.assertFalse(verify_password(wrong_password, hashed_password))

    def test_hash_uniqueness(self):
        """
        Test that hashing the same password twice results in different hashes.
        """
        password = "mypassword"
        hashed_password1 = hash_password(password)
        hashed_password2 = hash_password(password)

        # Check that the two hashes are not equal
        self.assertNotEqual(hashed_password1, hashed_password2)

if __name__ == "__main__":
    unittest.main()