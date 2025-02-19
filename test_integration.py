import unittest
from threading import Thread
import time
import socket
from chat import Server, Client

class TestIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Démarrer le serveur avant de lancer les tests"""
        cls.server = Server(port=5567)  # Utilisation d'un port dédié aux tests
        cls.server_thread = Thread(target=cls.server.start)
        cls.server_thread.daemon = True
        cls.server_thread.start()

        # Attendre que le serveur soit prêt
        start_time = time.time()
        while time.time() - start_time < 5:  # Timeout après 5 secondes
            try:
                with socket.create_connection(("127.0.0.1", 5566), timeout=1):
                    break  # Le serveur est prêt
            except (ConnectionRefusedError, socket.timeout):
                time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        """Arrêter le serveur après tous les tests"""
        cls.server.server.close()
        cls.server_thread.join(timeout=1)

    def test_client_to_client_communication(self):
        """Vérifier que deux clients peuvent communiquer via le serveur"""
        # Création des deux clients
        client1 = Client(port=5567)
        client2 = Client(port=5567)

        time.sleep(1)  # S'assurer que les clients sont bien connectés

        # Fonction pour écouter et vérifier la réception du message sur le client 2
        received_message = []

        def listen_for_message():
            message = client2.receive_messages()  # Attendre et recevoir le message
            received_message.append(message)

        # Lancer un thread pour écouter les messages du client 2
        listener_thread = Thread(target=listen_for_message)
        listener_thread.daemon = True
        listener_thread.start()

        # Envoyer un message du client 1
        client1.send_message("Hello from Client 1")

        # Attendre un peu pour que le message soit bien reçu
        time.sleep(1)

        # Vérifier que le message a bien été reçu
        listener_thread.join(timeout=2)  # Attendre que le thread ait fini de traiter
        self.assertIn("Hello from Client 1", received_message[0], "Le message n'a pas été correctement transmis")

        # Fermer les connexions client après le test
        client1.client.close()
        client2.client.close()

if __name__ == '__main__':
    unittest.main()
