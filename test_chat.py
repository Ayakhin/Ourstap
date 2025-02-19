import unittest
from unittest.mock import patch, MagicMock
import socket
from chat import Server, Client

class TestChatServer(unittest.TestCase):

    @patch('socket.socket')  # Mock the socket object
    def test_server_accepts_connections(self, mock_socket):
        """Test that the server accepts client connections"""
        mock_client_socket = MagicMock()
        mock_socket.return_value.accept.return_value = (mock_client_socket, ('127.0.0.1', 5555))

        server = Server()
        server_thread = patch.object(server, 'handle_client', return_value=None).start()  # Mock client handler

        # Simulate client connection
        server.start()

        self.assertTrue(mock_client_socket in server.clients)

    @patch('socket.socket')  # Mock the socket object
    def test_client_sends_and_receives_messages(self, mock_socket):
        """Test client sending and receiving messages"""
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.recv.return_value = b'{"message": "Hello, encrypted"}'

        client = Client()
        client.send_message("Test Message")

        mock_socket_instance.send.assert_called()  # Ensure message is sent
        self.assertEqual(client.receive_messages(), "Hello, encrypted")  # Simulate receiving message

if __name__ == '__main__':
    unittest.main()
