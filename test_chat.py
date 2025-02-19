import unittest
from threading import Thread
import time
from chat import Server, Client

class TestChatServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Start the server before running tests"""
        cls.server = Server()
        cls.server_thread = Thread(target=cls.server.start)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Give time for the server to start

    @classmethod
    def tearDownClass(cls):
        """Stop the server after all tests"""
        cls.server.server.close()
        cls.server_thread.join(timeout=1)

    def test_client_connection(self):
        """Test if a client can connect to the server"""
        client = Client()
        self.assertIsNotNone(client)  # Ensure the client object is created
        client.client.close()  # Close connection after test

    def test_client_message_exchange(self):
        """Test that a message is sent and received correctly"""
        client1 = Client()
        client2 = Client()

        client1.send_message("Hello from Client 1")
        time.sleep(1)  # Give time for message processing

        # Normally, we'd have to mock message retrieval, but this ensures message exchange works
        received_message = client2.receive_messages()
        self.assertIn("Hello from Client 1", received_message)

        client1.client.close()
        client2.client.close()

if __name__ == '__main__':
    unittest.main()
