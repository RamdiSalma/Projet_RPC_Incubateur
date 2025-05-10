import unittest
from controllers.rpc_server import check_temperature

class TestAlertes(unittest.TestCase):

    def test_temperature_basse(self):
        result = check_temperature(34.0)
        self.assertIn("basse", result.lower())

    def test_temperature_normale(self):
        result = check_temperature(36.5)
        self.assertIn("normale", result.lower())

    def test_temperature_elevee(self):
        result = check_temperature(38.0)
        self.assertIn("élevée", result.lower())

if __name__ == '__main__':
    unittest.main()
