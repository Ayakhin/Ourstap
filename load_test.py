from locust import User, task, between
import socket
import time

class ChatClient(User):
    wait_time = between(1, 3)
    host = "127.0.0.1"

    def on_start(self):
        """Se connecte au serveur de chat"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(("127.0.0.1", 5555))
            print("[INFO] Connexion au serveur réussie")
        except Exception as e:
            print(f"[ERROR] Échec de connexion au serveur: {e}")

    def on_stop(self):
        """Ferme la connexion"""
        self.client_socket.close()

    @task
    def send_message(self):
        """Envoie un message au serveur et enregistre la requête"""
        start_time = time.time()  # Début de la mesure du temps
        try:
            self.client_socket.send(b"Hello from Locust")
            response_time = int((time.time() - start_time) * 1000)  # Temps en millisecondes
            self.environment.events.request.fire(
                request_type="tcp",
                name="send_message",
                response_time=response_time,
                response_length=len("Hello from Locust"),
                exception=None
            )
            print("[INFO] Message envoyé")
        except Exception as e:
            response_time = int((time.time() - start_time) * 1000)
            self.environment.events.request.fire(
                request_type="tcp",
                name="send_message",
                response_time=response_time,
                response_length=0,
                exception=e
            )
            print(f"[ERROR] Impossible d'envoyer un message: {e}")
