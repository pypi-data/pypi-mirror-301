# memu/tests/test_auth.py
import unittest
from memu.auth import APIKeyManager

class TestAPIKeyManager(unittest.TestCase):
    def setUp(self):
        self.manager = APIKeyManager()

    def test_generate_and_validate_api_key(self):
        client_name = "TestClient"
        api_key = self.manager.generate_api_key(client_name)
        self.assertIsNotNone(api_key)
        valid_client = self.manager.validate_api_key(api_key)
        self.assertEqual(valid_client, client_name)

    def test_invalid_api_key(self):
        invalid_key = "invalid_api_key"
        self.assertIsNone(self.manager.validate_api_key(invalid_key))

if __name__ == '__main__':
    unittest.main()
