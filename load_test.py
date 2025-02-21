from locust import HttpUser, task, between

class ChatUser(HttpUser):
    wait_time = between(1, 3)  # Pause entre les requêtes

    @task
    def send_message(self):
        """Simule l'envoi d'un message par un utilisateur"""
        payload = {
            "username": "test_user",
            "message": "Hello from Locust!"
        }
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/send", json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Erreur : {response.status_code}, {response.text}")

    @task
    def get_messages(self):
        """Simule la récupération des messages"""
        response = self.client.get("/messages")
        if response.status_code != 200:
            print(f"Erreur : {response.status_code}, {response.text}")

if __name__ == "__main__":
    import os
    os.system("locust -f load_test.py --host=http://127.0.0.1:5555")
