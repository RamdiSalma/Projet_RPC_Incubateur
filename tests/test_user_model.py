import unittest
from models.user_model import verify_login

class TestUserModel(unittest.TestCase):

    def test_connexion_valide(self):
        self.assertTrue(verify_login("admin", "admin"))  # Mettre un utilisateur réel

    def test_connexion_invalide(self):
        self.assertFalse(verify_login("fake", "wrong"))

if __name__ == '__main__':
    unittest.main()
