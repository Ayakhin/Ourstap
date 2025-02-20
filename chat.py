import socket
import threading
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import base64

# Fonction pour générer une paire de clés RSA
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Fonction pour chiffrer avec RSA
def encrypt_rsa(public_key, message):
    try:
        recipient_key = RSA.import_key(public_key)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        encrypted_message = cipher_rsa.encrypt(message)
        return base64.b64encode(encrypted_message).decode('utf-8')
    except (ValueError, TypeError):
        print("[ERREUR] Échec du chiffrement RSA.")
        return None

# Fonction pour déchiffrer avec RSA
def decrypt_rsa(private_key, encrypted_message):
    try:
        private_key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher_rsa.decrypt(base64.b64decode(encrypted_message))
        return decrypted_message
    except (ValueError, TypeError):
        print("[ERREUR] Échec du déchiffrement RSA.")
        return None

# Fonction pour chiffrer un message avec AES
def encrypt_aes(aes_key, message):
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message)
    return base64.b64encode(cipher_aes.nonce + tag + ciphertext).decode('utf-8')

# Fonction pour déchiffrer un message avec AES
def decrypt_aes(aes_key, encrypted_message):
    try:
        encrypted_message = base64.b64decode(encrypted_message)
        nonce = encrypted_message[:16]
        tag = encrypted_message[16:32]
        ciphertext = encrypted_message[32:]
        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        return cipher_aes.decrypt_and_verify(ciphertext, tag)
    except (ValueError, KeyError):
        print("[ERREUR] Échec du déchiffrement AES.")
        return None

# Classe serveur
class Server:
    def __init__(self, host='0.0.0.0', port=5555):  # Écoute sur 0.0.0.0 pour Docker
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = []
        self.aes_key = get_random_bytes(16)
        print(f"Serveur en écoute sur {host}:{port}")

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)
                except:
                    client.close()
                    self.clients.remove(client)

    def handle_client(self, client_socket):
        try:
            client_public_key = client_socket.recv(1024)
            if not client_public_key:
                print("[ERREUR] Clé publique non reçue.")
                return

            encrypted_aes_key = encrypt_rsa(client_public_key, self.aes_key)
            if encrypted_aes_key:
                client_socket.send(encrypted_aes_key.encode('utf-8'))

            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                self.broadcast(message, client_socket)
        except (ConnectionResetError, ConnectionAbortedError):
            print("[INFO] Client déconnecté.")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def start(self):
        while True:
            client_socket, _ = self.server.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

# Classe client
class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((host, port))
        except ConnectionRefusedError:
            print("[ERREUR] Impossible de se connecter au serveur.")
            return

        self.private_key, self.public_key = generate_rsa_keys()
        self.client.send(self.public_key)

        encrypted_aes_key = self.client.recv(1024).decode('utf-8')
        self.aes_key = decrypt_rsa(self.private_key, encrypted_aes_key)

        print("Connecté au serveur !")
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.run()

    def send_message(self, message):
        if self.aes_key:
            encrypted_message = encrypt_aes(self.aes_key, message.encode('utf-8'))
            self.client.send(json.dumps({"message": encrypted_message}).encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                if not data:
                    break
                data = json.loads(data)
                decrypted_message = decrypt_aes(self.aes_key, data["message"]).decode('utf-8')
                print("Message reçu :", decrypted_message)
            except:
                self.client.close()
                break

    def run(self):
        while True:
            message = input("You: ")
            if message.lower() == "exit":
                print("Déconnexion...")
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
