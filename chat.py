import socket
import threading
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes


# Fonction pour générer une paire de clés RSA
def generate_rsa_keys():
    key = RSA.generate(2048)  # Génère une paire de clés RSA de 2048 bits
    private_key = key.export_key()  # Exporte la clé privée
    public_key = key.publickey().export_key()  # Exporte la clé publique associée
    return private_key, public_key


# Fonction pour chiffrer avec RSA
def encrypt_rsa(public_key, message):
    recipient_key = RSA.import_key(public_key)  # Importation de la clé publique
    cipher_rsa = PKCS1_OAEP.new(recipient_key)  # Chiffreur RSA avec OAEP
    encrypted_message = cipher_rsa.encrypt(message)  # Chiffrement du message
    return base64.b64encode(encrypted_message).decode('utf-8')


# Fonction pour déchiffrer avec RSA
def decrypt_rsa(private_key, encrypted_message):
    private_key = RSA.import_key(private_key)  # Importation de la clé privée
    cipher_rsa = PKCS1_OAEP.new(private_key)  # Déchiffreur RSA avec OAEP
    decrypted_message = cipher_rsa.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message


# Fonction pour chiffrer un message avec AES
def encrypt_aes(aes_key, message):
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message)
    return base64.b64encode(cipher_aes.nonce + tag + ciphertext).decode('utf-8')


# Fonction pour déchiffrer un message avec AES
def decrypt_aes(aes_key, encrypted_message):
    encrypted_message = base64.b64decode(encrypted_message)
    nonce = encrypted_message[:16]  # Extraction du nonce
    tag = encrypted_message[16:32]  # Extraction du tag
    ciphertext = encrypted_message[32:]  # Texte chiffré restant
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    return cipher_aes.decrypt_and_verify(ciphertext, tag)

class Server:
    def __init__(self, host='0.0.0.0', port=5555):  # Changer '127.0.0.1' en '0.0.0.0'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = []
        self.aes_key = get_random_bytes(16)
        print(f"Server listening on {host}:{port}")

    def broadcast(self, message, client_socket):
        print(f"[DEBUG] Relayed message (encrypted): {message}")
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)
                except OSError:
                    client.close()
                    self.clients.remove(client)

    # Fonction pour gérer un client connecté
    def handle_client(self, client_socket):
        client_public_key = client_socket.recv(1024)
        encrypted_aes_key = encrypt_rsa(client_public_key, self.aes_key)
        client_socket.send(encrypted_aes_key.encode('utf-8'))

        while True:
            try:
                message = client_socket.recv(1024)
                self.broadcast(message, client_socket)
            except OSError:
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def start(self):
        while True:
            client_socket, _ = self.server.accept()
            self.clients.append(client_socket)
            threading.Thread(
                target=self.handle_client, args=(client_socket,)
            ).start()

class Client:
    def __init__(self, host='chat-server', port=5555):  # Changer '127.0.0.1' en 'chat-server'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))  # Connexion au serveur

        self.private_key, self.public_key = generate_rsa_keys()
        self.client.send(self.public_key)

        encrypted_aes_key = self.client.recv(1024).decode('utf-8')
        self.aes_key = decrypt_rsa(self.private_key, encrypted_aes_key)

        print("Connected to the server!")
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.run()

    # Envoi des messages au serveur
    def send_message(self, message):
        encrypted_message = encrypt_aes(self.aes_key, message.encode('utf-8'))
        print("Message chiffré envoyé AES:", encrypted_message)
        self.client.send(json.dumps({"message": encrypted_message}).encode('utf-8'))

    # Réception des messages du serveur
    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                data = json.loads(data)
                print("Message reçu chiffré:", data)
                decrypted_message = decrypt_aes(
                    self.aes_key, data["message"]
                ).decode('utf-8')
                print("Message reçu :", decrypted_message)
            except OSError:
                self.client.close()
                break

    def run(self):
        while True:
            message = input("You: ")
            if message.lower() == "exit":
                print("Disconnecting...")
                self.client.close()
                break
            self.send_message(message)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python chat.py [server/client]")
    elif sys.argv[1] == "server":
        Server().start()
    elif sys.argv[1] == "client":
        Client()
