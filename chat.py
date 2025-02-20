import socket
import threading
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import base64

# Fonction pour generer une paire de clés RSA
def generate_rsa_keys():
    key = RSA.generate(2048)  # Génère une paire de clés RSA de 2048 bits
    private_key = key.export_key()  # Exporte la clé privée
    public_key = key.publickey().export_key()  # Exporte la clé publique associée
    return private_key, public_key


# Fonction pour chiffrer avec RSA
def encrypt_rsa(public_key, message):
    recipient_key = RSA.import_key(public_key)  # Importation de la clé publique
    cipher_rsa = PKCS1_OAEP.new(recipient_key)  # Création du chiffreur RSA avec OAEP
    encrypted_message = cipher_rsa.encrypt(message)  # Chiffrement du message
    return base64.b64encode(encrypted_message).decode('utf-8')  # Encodage en base64 pour transmission

# Fonction pour déchiffrer avec RSA
def decrypt_rsa(private_key, encrypted_message):
    private_key = RSA.import_key(private_key)  # Importation de la clé privée
    cipher_rsa = PKCS1_OAEP.new(private_key)  # Création du déchiffreur RSA avec OAEP
    decrypted_message = cipher_rsa.decrypt(base64.b64decode(encrypted_message))  # Décodage Base64 puis déchiffrement
    return decrypted_message 

# Fonction pour chiffrer un message avec AES
def encrypt_aes(aes_key, message):
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)  # Création du chiffreur AES en mode EAX (sécurisé)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message)  # Chiffrement du message + tag d'authentification
    return base64.b64encode(cipher_aes.nonce + tag + ciphertext).decode('utf-8')  # Encodage Base64 pour transmission

# Fonction pour déchiffrer un message avec AES
def decrypt_aes(aes_key, encrypted_message):
    encrypted_message = base64.b64decode(encrypted_message)  # Décodage Base64 du message chiffré
    nonce = encrypted_message[:16]  # Extraction du nonce (16 premiers octets)
    tag = encrypted_message[16:32]  # Extraction du tag d'authentification (16 octets suivants)
    ciphertext = encrypted_message[32:]  # Récupération du texte chiffré restant
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)  # Création du déchiffreur AES avec le nonce
    return cipher_aes.decrypt_and_verify(ciphertext, tag)  # Déchiffrement et vérification du tag

class Server:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création du socket TCP
        self.server.bind((host, port))  # Attache le serveur à l'adresse et au port
        self.server.listen(5)  # Écoute jusqu'à 5 connexions simultanées
        self.clients = []  # Liste des clients connectés
        self.aes_key = get_random_bytes(16)  # Génère une clé AES aléatoire pour les échanges sécurisés
        print(f"Server listening on {host}:{port}")  # Affichage du démarrage du serveur

    def broadcast(self, message, client_socket):
        print(f"[DEBUG] Relayed message (encrypted): {message}")  # Affichage du message chiffré
        for client in self.clients:
            if client != client_socket:  # Ne pas renvoyer le message à l'expéditeur
                try:
                    client.send(message)  # Envoie le message aux autres clients
                except:
                    client.close()  # Ferme la connexion en cas d'erreur
                    self.clients.remove(client)  # Supprime le client de la liste

 # Fonction pour gérer un client connecté
    def handle_client(self, client_socket):
        client_public_key = client_socket.recv(1024)  # Réception de la clé publique du client
        encrypted_aes_key = encrypt_rsa(client_public_key, self.aes_key)  # Chiffrement de la clé AES avec RSA
        client_socket.send(encrypted_aes_key.encode('utf-8'))  # Envoi de la clé AES chiffrée au client

        while True:
            try:
                message = client_socket.recv(1024)  # Réception d'un message chiffré du client
                self.broadcast(message, client_socket)  # Diffusion du message aux autres clients
            except:
                self.clients.remove(client_socket)  # Retrait du client en cas de déconnexion
                client_socket.close()  # Fermeture de la connexion
                break  # Sortie de la boucle

    def start(self):
        while True:
            client_socket, _ = self.server.accept()  # Accepte une nouvelle connexion client
            self.clients.append(client_socket)  # Ajoute le client à la liste
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()  # Lance un thread pour gérer le client


class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création du socket client
        self.client.connect((host, port))  # Connexion au serveur
        self.private_key, self.public_key = generate_rsa_keys()  # Génération des clés RSA du client
        self.client.send(self.public_key)  # Envoi de la clé publique au serveur

        encrypted_aes_key = self.client.recv(1024).decode('utf-8')  # Réception de la clé AES chiffrée
        self.aes_key = decrypt_rsa(self.private_key, encrypted_aes_key)  # Déchiffrement de la clé AES avec RSA

        print("Connected to the server!")  # Confirmation de connexion
        threading.Thread(target=self.receive_messages, daemon=True).start()  # Lancement du thread de réception
        self.run()  # Démarrage de la boucle utilisateur

# Envoi des messages au serveur
    def send_message(self, message):
        encrypted_message = encrypt_aes(self.aes_key, message.encode('utf-8'))  # Chiffrement du message avec AES
        print("Message chiffré envoyé AES:", encrypted_message)  # Affichage du message déchiffré                
        self.client.send(json.dumps({"message": encrypted_message}).encode('utf-8'))  # Envoi du message sous format JSON
        

# Réception des messages du serveur
    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')  # Réception et décodage du message
                data = json.loads(data)  # Chargement du JSON
                print("Message reçu chiffré:", data)  # Affichage du message déchiffré                
                decrypted_message = decrypt_aes(self.aes_key, data["message"]).decode('utf-8')  # Déchiffrement
                print("Message reçu :", decrypted_message)  # Affichage du message déchiffré
            except:
                self.client.close()  # Fermeture du socket en cas d'erreur
                break  # Sortie de la boucle

    def run(self):
        while True:
            message = input("You: ")  # Récupération du message de l'utilisateur
            if message.lower() == "exit":  # Si l'utilisateur tape "exit", il se déconnecte
                print("Disconnecting...")
                self.client.close()
                break
            self.send_message(message)  # Envoi du message chiffré




if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:  # Vérification des arguments
        print("Usage: python chat.py [server/client]")  # Message d'aide
    elif sys.argv[1] == "server":
        Server().start()  # Lancement du serveur
    elif sys.argv[1] == "client":
        Client()  # Lancement du client
