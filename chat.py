import socket
import threading
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import base64

# Génération de la clé RSA pour chaque client

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Chiffrement RSA
def encrypt_rsa(public_key, message):
    recipient_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_message = cipher_rsa.encrypt(message)
    return base64.b64encode(encrypted_message).decode('utf-8')

# Déchiffrement RSA
def decrypt_rsa(private_key, encrypted_message):
    private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher_rsa.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message

# Chiffrement AES
def encrypt_aes(aes_key, message):
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message)
    return base64.b64encode(cipher_aes.nonce + tag + ciphertext).decode('utf-8')

# Déchiffrement AES
def decrypt_aes(aes_key, encrypted_message):
    encrypted_message = base64.b64decode(encrypted_message)
    nonce = encrypted_message[:16]
    tag = encrypted_message[16:32]
    ciphertext = encrypted_message[32:]
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    return cipher_aes.decrypt_and_verify(ciphertext, tag)

# Serveur
class Server:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = []
        self.aes_key = get_random_bytes(16)  # Clé AES partagée
        print(f"Serveur en écoute sur {host}:{port}")

    def broadcast(self, message, client_socket):
        print(f"[DEBUG] Message relayé par le serveur (chiffré) : {message}")
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)
                except:
                    client.close()
                    self.clients.remove(client)

    def handle_client(self, client_socket):
        client_public_key = client_socket.recv(1024)  # Récupère la clé publique du client
        encrypted_aes_key = encrypt_rsa(client_public_key, self.aes_key)
        client_socket.send(encrypted_aes_key.encode('utf-8'))

        while True:
            try:
                message = client_socket.recv(1024)
                self.broadcast(message, client_socket)
            except:
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def start(self):
        while True:
            client_socket, _ = self.server.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

# Client
class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.private_key, self.public_key = generate_rsa_keys()
        self.client.send(self.public_key)  # Envoi de la clé publique au serveur
        encrypted_aes_key = self.client.recv(1024).decode('utf-8')
        self.aes_key = decrypt_rsa(self.private_key, encrypted_aes_key)
        print("Connecté au serveur !")
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.run()
    
    def send_message(self, message):
        print(f"[DEBUG] Message original : {message}")
        encrypted_message = encrypt_aes(self.aes_key, message.encode('utf-8'))
        print(f"[DEBUG] Message chiffré AES : {encrypted_message}")
        self.client.send(json.dumps({"message": encrypted_message}).encode('utf-8'))
    
    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                print(f"[DEBUG] Message chiffré reçu : {data}")
                if not data:
                    break
                data = json.loads(data)
                message = decrypt_aes(self.aes_key, data["message"]).decode('utf-8')
                print(f"[DEBUG] Message déchiffré : {message}")
                print("Message reçu:", message)
            except:
                print("Connexion perdue avec le serveur.")
                self.client.close()
                break
    
    def run(self):
        while True:
            message = input("Vous : ")
            self.send_message(message)

# Exécution du script
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Utilisation : python script.py [server/client]")
    elif sys.argv[1] == "server":
        server = Server()
        server.start()
    elif sys.argv[1] == "client":
        Client()