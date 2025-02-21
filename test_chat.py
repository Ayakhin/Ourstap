import unittest
import threading
import time
from chat import Server

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Démarre le serveur en arrière-plan avant les tests"""
        cls.server = Server(port=5567)  # Utilise un port différent pour éviter les conflits
        cls.server_thread = threading.Thread(target=cls.server.start, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Attendre que le serveur démarre bien

    @classmethod
    def tearDownClass(cls):
        """Arrête proprement le serveur après les tests"""
        cls.server.server.close()  # Fermer le socket du serveur
        cls.server_thread.join(timeout=1)  # Attendre que le thread se termine

    def test_server_running(self):
        """Vérifie si le serveur tourne bien"""
        self.assertTrue(self.server.server)

if __name__ == "__main__":
    unittest.main()
