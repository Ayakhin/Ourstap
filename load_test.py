from locust import HttpUser, task, between
import socket
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import base64

class ChatClient(HttpUser):
    wait_time = between(1, 3)  # Simulation d'un délai entre les requêtes

    def on_start(self):
        """Se connecte au serveur de chat lors du démarrage du test"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 5555))

        # Génération des clés RSA
        self.private_key, self.public_key = self.generate_rsa_keys()
        self.client_socket.send(self.public_key)

        # Récupération et déchiffrement de la clé AES
        encrypted_aes_key = self.client_socket.recv(1024).decode("utf-8")
        self.aes_key = self.decrypt_rsa(self.private_key, encrypted_aes_key)

    def on_stop(self):
        """Ferme la connexion au serveur lors de l'arrêt du test"""
        self.client_socket.close()

    def generate_rsa_keys(self):
        """Génère une paire de clés RSA"""
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    def decrypt_rsa(self, private_key, encrypted_message):
        """Déchiffre un message RSA"""
        private_key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher_rsa.decrypt(base64.b64decode(encrypted_message))
        return decrypted_message

    def encrypt_aes(self, message):
        """Chiffre un message avec AES"""
        cipher_aes = AES.new(self.aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode("utf-8"))
        return base64.b64encode(cipher_aes.nonce + tag + ciphertext).decode("utf-8")

    @task
    def send_message(self):
        """Envoie un message au serveur"""
        message = self.encrypt_aes("Test de performance avec Locust")
        self.client_socket.send(json.dumps({"message": message}).encode("utf-8"))
