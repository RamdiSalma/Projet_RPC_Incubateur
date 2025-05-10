import unittest
from backend.gestion_temperature import verifier_temperature, lire_temperature_capteur

class TestGestionTemperature(unittest.TestCase):

    def test_temperature_inférieure_au_seuil(self):
        # Cas où la température est normale
        self.assertFalse(verifier_temperature(36.5, seuil=37.5))

    def test_temperature_égale_au_seuil(self):
        # Cas limite, ne devrait pas déclencher d'alerte
        self.assertFalse(verifier_temperature(37.5, seuil=37.5))

    def test_temperature_supérieure_au_seuil(self):
        # Cas où la température dépasse le seuil
        self.assertTrue(verifier_temperature(39.2, seuil=37.5))

    def test_temperature_négative(self):
        # Cas improbable, mais on le teste pour robustesse
        self.assertFalse(verifier_temperature(-5.0, seuil=37.5))

    def test_temperature_depuis_capteur(self):
        # Test que la fonction retourne bien un float
        temp = lire_temperature_capteur()
        self.assertIsInstance(temp, float)

if __name__ == '__main__':
    unittest.main()
