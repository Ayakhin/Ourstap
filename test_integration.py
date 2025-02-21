import unittest
import threading
import time
from chat import Server, Client

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Démarre un serveur avant les tests d'intégration"""
        cls.server = Server(port=5567)  # Utiliser un port spécifique
        cls.server_thread = threading.Thread(target=cls.server.start, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Attendre que le serveur démarre bien

    @classmethod
    def tearDownClass(cls):
        """Ferme le serveur proprement après les tests"""
        cls.server.server.close()
        cls.server_thread.join(timeout=1)

    def test_client_to_client_communication(self):
        """Vérifier que deux clients peuvent communiquer via le serveur"""
        client1 = Client(host="127.0.0.1", port=5567)
        client2 = Client(host="127.0.0.1", port=5567)

        client1.send_message("Hello from client1")
        received_message = client2.receive_messages()

        self.assertIn("Hello from client1", received_message)

if __name__ == "__main__":
    unittest.main()
    