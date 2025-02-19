import unittest
from threading import Thread
import time
from chat import Server, Client

class TestIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Start the server before running tests"""
        cls.server = Server(port=5566)  # Use a different port for testing
        cls.server_thread = Thread(target=cls.server.start)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Allow server to initialize

    @classmethod
    def tearDownClass(cls):
        """Stop the server after all tests"""
        cls.server.server.close()
        cls.server_thread.join(timeout=1)

    def test_client_to_client_communication(self):
        """Test that two clients can communicate through the server"""
        client1 = Client(port=5566, interactive=False)
        client2 = Client(port=5566, interactive=False)

        time.sleep(1)  # Ensure both clients are connected before sending messages

        client1.send_message("Hello from Client 1")
        time.sleep(1)  # Allow message processing

        received_message = client2.receive_messages()
        self.assertEqual(received_message, "Hello from Client 1")

        client1.client.close()
        client2.client.close()

if __name__ == '__main__':
    unittest.main()
