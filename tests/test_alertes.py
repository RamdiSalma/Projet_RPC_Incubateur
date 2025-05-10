import unittest
from backend.alertes import generer_alerte, Alerte

class TestAlertes(unittest.TestCase):

    def test_generation_alerte_haute_temperature(self):
        temp = 39.0
        seuil = 37.5
        alerte = generer_alerte(temp, seuil)

        self.assertIsInstance(alerte, Alerte)
        self.assertEqual(alerte.type, "Température élevée")
        self.assertEqual(alerte.valeur, temp)
        self.assertIn("dépassement", alerte.message.lower())

    def test_alerte_pas_de_debordement(self):
        temp = 36.0
        seuil = 37.5
        alerte = generer_alerte(temp, seuil)

        self.assertIsNone(alerte)  # pas d'alerte si la température est normale

    def test_alerte_limite_exacte(self):
        temp = 37.5
        seuil = 37.5
        alerte = generer_alerte(temp, seuil)

        self.assertIsNone(alerte)  # seuil exact ne doit pas déclencher

if __name__ == '__main__':
    unittest.main()
