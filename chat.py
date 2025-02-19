import socket 
import threading
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes 
import base64 

# Fonction pour générer une paire de clés RSA (privée et publique)
def generate_rsa_keys():
    key = RSA.generate(2048)  # Génération d'une clé RSA de 2048 bits
    private_key = key.export_key()  
    public_key = key.publickey().export_key()
    return private_key, public_key

# Fonction pour chiffrer un message avec RSA
def encrypt_rsa(public_key, message):
    recipient_key = RSA.import_key(public_key)  # Importation de la clé publique du destinataire
    cipher_rsa = PKCS1_OAEP.new(recipient_key)  # Création du chiffreur RSA avec le mode OAEP
    encrypted_message = cipher_rsa.encrypt(message)  # Chiffrement du message
    return base64.b64encode(encrypted_message).decode('utf-8')  # Encodage en base64 et conversion en texte

# Fonction pour déchiffrer un message avec RSA
def decrypt_rsa(private_key, encrypted_message):
    private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)  # Création du déchiffreur RSA avec le mode OAEP
    decrypted_message = cipher_rsa.decrypt(base64.b64decode(encrypted_message))  # Décodage base64 et déchiffrement
    return decrypted_message

# Fonction pour chiffrer un message avec AES
def encrypt_aes(aes_key, message):
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)  # Création du chiffreur AES en mode EAX
    ciphertext, tag = cipher_aes.encrypt_and_digest(message)  # Chiffrement et génération du tag d'authentification
    return base64.b64encode(cipher_aes.nonce + tag + ciphertext).decode('utf-8')  # Retourne les données chiffrées en base64

# Fonction pour déchiffrer un message avec AES
def decrypt_aes(aes_key, encrypted_message):
    encrypted_message = base64.b64decode(encrypted_message)  # Décodage de la base64
    nonce = encrypted_message[:16]  # Extraction du nonce (16 premiers octets)
    tag = encrypted_message[16:32]  # Extraction du tag d'authentification (16 octets suivants)
    ciphertext = encrypted_message[32:]  # Extraction du texte chiffré
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)  # Recréation du chiffreur AES
    return cipher_aes.decrypt_and_verify(ciphertext, tag)  # Déchiffrement et vérification d'intégrité

# Classe du serveur
class Server:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création du socket TCP
        self.server.bind((host, port))
        self.server.listen(5)  # Mise en écoute du serveur, avec un maximum de 5 connexions en attente
        self.clients = []  # Liste pour stocker les clients connectés
        self.aes_key = get_random_bytes(16)  # Génération d'une clé AES de 16 octets
        print(f"Serveur en écoute sur {host}:{port}")

    # Fonction pour envoyer un message chiffré à tous les clients connectés
    def broadcast(self, message, client_socket):
        print(f"[DEBUG] Message relayé par le serveur (chiffré) : {message}")
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)  # Envoi du message chiffré
                except:
                    client.close()
                    self.clients.remove(client)  # Suppression du client en cas d'erreur

    # Fonction pour gérer un client connecté
    def handle_client(self, client_socket):
        client_public_key = client_socket.recv(1024)  # Récupération de la clé publique du client
        encrypted_aes_key = encrypt_rsa(client_public_key, self.aes_key)  # Chiffrement de la clé AES avec RSA
        client_socket.send(encrypted_aes_key.encode('utf-8'))  # Envoi de la clé AES chiffrée au client
        
        while True:
            try:
                message = client_socket.recv(1024)  # Réception du message chiffré du client
                self.broadcast(message, client_socket)  # Transmission aux autres clients
            except:
                self.clients.remove(client_socket)
                client_socket.close()
                break

    # Démarrage du serveur
    def start(self):
        while True:
            client_socket, _ = self.server.accept()  # Acceptation d'une nouvelle connexion client
            self.clients.append(client_socket)  # Ajout du client à la liste des clients connectés
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()  # Lancement du thread client

# Classe du client
class Client:
    def __init__(self, host='127.0.0.1', port=5555, interactive=True):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.private_key, self.public_key = generate_rsa_keys()
        self.client.send(self.public_key)
        encrypted_aes_key = self.client.recv(1024).decode('utf-8')
        self.aes_key = decrypt_rsa(self.private_key, encrypted_aes_key)
        print("Connecté au serveur !")

        threading.Thread(target=self.receive_messages, daemon=True).start()

        # Only enter interactive mode for manual users
        if interactive:
            self.run()

    def send_message(self, message):
        encrypted_message = encrypt_aes(self.aes_key, message.encode('utf-8'))
        self.client.send(json.dumps({"message": encrypted_message}).encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"[DEBUG] Message chiffré reçu : {data}")

                data = json.loads(data)
                message = decrypt_aes(self.aes_key, data["message"]).decode('utf-8')

                print(f"[DEBUG] Message déchiffré : {message}")
                print("Message reçu:", message)

                return message  # Allows tests to verify received messages
            except:
                self.client.close()
                break


# Exécution principale
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "server":
        Server().start()
    elif sys.argv[1] == "client":
        Client()
