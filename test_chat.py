import unittest
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import base64
from chat import encrypt_rsa, decrypt_rsa, encrypt_aes, decrypt_aes  # Import functions from chat.py

class TestCryptoFunctions(unittest.TestCase):

    def setUp(self):
        """Set up keys for encryption tests"""
        self.private_key, self.public_key = self.generate_keys()
        self.aes_key = get_random_bytes(16)  # Generate a new AES key
        self.message = b"Hello, this is a secure message!"

    def generate_keys(self):
        """Generate RSA key pair"""
        key = RSA.generate(2048)
        return key.export_key(), key.publickey().export_key()

    def test_rsa_encryption_decryption(self):
        """Test RSA encryption and decryption"""
        encrypted_message = encrypt_rsa(self.public_key, self.aes_key)
        decrypted_message = decrypt_rsa(self.private_key, encrypted_message)
        self.assertEqual(decrypted_message, self.aes_key)

    def test_aes_encryption_decryption(self):
        """Test AES encryption and decryption"""
        encrypted_message = encrypt_aes(self.aes_key, self.message)
        decrypted_message = decrypt_aes(self.aes_key, encrypted_message)
        self.assertEqual(decrypted_message, self.message)

if __name__ == "__main__":
    unittest.main()
