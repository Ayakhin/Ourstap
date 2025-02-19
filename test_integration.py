import unittest
from threading import Thread
from chat import Server, Client
import time

class TestIntegration(unittest.TestCase):

    def setUp(self):
        """Start server in a separate thread before each test"""
        self.server = Server()
        self.server_thread = Thread(target=self.server.start)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(1)  # Allow server to initialize

    def test_client_to_client_communication(self):
        """Test that two clients can communicate through the server"""
        client1 = Client()
        client2 = Client()

        client1.send_message("Hello from Client 1")
        time.sleep(1)  # Allow message to process

        self.assertEqual(client2.receive_messages(), "Hello from Client 1")

    def tearDown(self):
        """Close server after tests"""
        self.server.server.close()

if __name__ == '__main__':
    unittest.main()
