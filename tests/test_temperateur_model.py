import unittest
from Model.temperature import save_temperature, get_latest_temperature

class TestTemperatureModel(unittest.TestCase):

    def test_enregistrement_temperature(self):
        save_temperature(36.8)  # Doit s'insérer sans erreur

    def test_recuperation_temperature(self):
        value, timestamp = get_latest_temperature()
        self.assertIsInstance(value, float)
        self.assertIsNotNone(timestamp)

if __name__ == '__main__':
    unittest.main()
