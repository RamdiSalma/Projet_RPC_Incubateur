import unittest
from xmlrpc.client import ServerProxy

class TestRPCClient(unittest.TestCase):

    def setUp(self):
        self.rpc = ServerProxy("http://localhost:8000")

    def test_save_temperature_rpc(self):
        result = self.rpc.save_temperature(37.1)
        self.assertIsNone(result)  # fonction ne retourne rien

    def test_get_latest_temperature_rpc(self):
        value, timestamp = self.rpc.get_latest_temperature()
        self.assertIsInstance(value, float)

    def test_check_temperature_rpc(self):
        result = self.rpc.check_temperature(39.0)
        self.assertIn("élevée", result.lower())

if __name__ == '__main__':
    unittest.main()
