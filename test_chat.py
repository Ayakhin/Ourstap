import unittest
from chat import encrypt_rsa, decrypt_rsa, encrypt_aes, decrypt_aes, generate_rsa_keys
from Crypto.Random import get_random_bytes

class TestCryptoFunctions(unittest.TestCase):

    def setUp(self):
        """Set up keys and sample data for testing"""
        self.private_key, self.public_key = generate_rsa_keys()
        self.aes_key = get_random_bytes(16)
        self.message = b"Hello, Secure Chat!"

    def test_rsa_encryption_decryption(self):
        """Ensure RSA encryption and decryption work correctly"""
        encrypted_message = encrypt_rsa(self.public_key, self.aes_key)
        decrypted_message = decrypt_rsa(self.private_key, encrypted_message)
        self.assertEqual(decrypted_message, self.aes_key)

    def test_aes_encryption_decryption(self):
        """Ensure AES encryption and decryption work correctly"""
        encrypted_message = encrypt_aes(self.aes_key, self.message)
        decrypted_message = decrypt_aes(self.aes_key, encrypted_message)
        self.assertEqual(decrypted_message, self.message)

if __name__ == "__main__":
    unittest.main()
