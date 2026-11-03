"""
Unit Tests for Caesar Cipher Implementation
Cyber Security Project 2 - Basic Encryption & Decryption

Covers all required test cases specified in the project requirements:
1. "HELLO WORLD" with key 3 -> "KHOOR ZRUOG" -> "HELLO WORLD"
2. "xyz" with key 3 -> "abc" -> "xyz" (lowercase wraparound)
3. Mixed case preservation (e.g. "HeLLo" with key 2 -> "JgNNq" -> "HeLLo")
4. Preservation of spaces, punctuation, numbers, and symbols
5. Key 0 returning the exact same text
6. Key larger than 26 behaving correctly (modulo 26 normalization)
7. Negative key handled consistently
8. Empty text handling
9. Invalid shift-key and non-string input validation
"""

import sys
from pathlib import Path
import unittest

# Ensure the directory containing cipher.py is in sys.path
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from cipher import encrypt, decrypt, normalize_shift


class TestCaesarCipher(unittest.TestCase):

    def test_standard_spec_hello_world(self):
        """Test spec case: 'HELLO WORLD' with key 3 -> 'KHOOR ZRUOG' -> 'HELLO WORLD'."""
        original = "HELLO WORLD"
        key = 3
        ciphertext = encrypt(original, key)
        self.assertEqual(ciphertext, "KHOOR ZRUOG")
        decrypted = decrypt(ciphertext, key)
        self.assertEqual(decrypted, original)

    def test_lowercase_wraparound_xyz(self):
        """Test spec case: 'xyz' with key 3 -> 'abc' -> 'xyz'."""
        original = "xyz"
        key = 3
        ciphertext = encrypt(original, key)
        self.assertEqual(ciphertext, "abc")
        decrypted = decrypt(ciphertext, key)
        self.assertEqual(decrypted, original)

    def test_mixed_case_preservation(self):
        """Test spec case: 'HeLLo' with key 2 preserves case -> 'JgNNq'."""
        original = "HeLLo"
        key = 2
        ciphertext = encrypt(original, key)
        self.assertEqual(ciphertext, "JgNNq")
        decrypted = decrypt(ciphertext, key)
        self.assertEqual(decrypted, original)

    def test_spaces_punctuation_numbers_preserved(self):
        """Test spec case: spaces, punctuation, numbers, and symbols remain untouched."""
        original = "Cyber Security #2: Caesar 101, Test! @2026."
        key = 5
        ciphertext = encrypt(original, key)
        # Only alphabetic letters should shift; punctuation, numbers, spaces stay intact
        self.assertTrue("101" in ciphertext)
        self.assertTrue("@2026." in ciphertext)
        self.assertTrue("#2:" in ciphertext)
        decrypted = decrypt(ciphertext, key)
        self.assertEqual(decrypted, original)

    def test_key_zero_identity(self):
        """Test spec case: key 0 returns the identical text."""
        original = "Antigravity Secure System 42!"
        self.assertEqual(encrypt(original, 0), original)
        self.assertEqual(decrypt(original, 0), original)

    def test_key_larger_than_26(self):
        """Test spec case: key > 26 wraps correctly via modulo 26."""
        original = "Hello World"
        key_standard = 3
        key_large = 29  # 29 % 26 == 3
        key_huge = 107  # 107 % 26 == 3

        cipher_standard = encrypt(original, key_standard)
        cipher_large = encrypt(original, key_large)
        cipher_huge = encrypt(original, key_huge)

        self.assertEqual(cipher_standard, cipher_large)
        self.assertEqual(cipher_standard, cipher_huge)
        self.assertEqual(decrypt(cipher_large, key_large), original)

    def test_negative_key(self):
        """Test spec case: negative keys are handled consistently."""
        original = "Attack at dawn"
        key_neg = -3
        # Negative shift of -3 is equivalent to positive shift of +23
        ciphertext = encrypt(original, key_neg)
        self.assertEqual(ciphertext, encrypt(original, 23))
        self.assertEqual(decrypt(ciphertext, key_neg), original)

    def test_empty_string(self):
        """Test spec case: empty string returns empty string without crashing."""
        self.assertEqual(encrypt("", 3), "")
        self.assertEqual(decrypt("", 3), "")

    def test_shift_normalization_and_validation(self):
        """Test shift normalization and invalid input handling."""
        self.assertEqual(normalize_shift(3), 3)
        self.assertEqual(normalize_shift(29), 3)
        self.assertEqual(normalize_shift(-3), 23)
        self.assertEqual(normalize_shift("5"), 5)
        self.assertEqual(normalize_shift("-5"), 21)

        # Invalid string shift
        with self.assertRaises(ValueError):
            normalize_shift("not_a_number")

        # Decimal float shift
        with self.assertRaises(ValueError):
            normalize_shift(3.14)

    def test_invalid_text_type(self):
        """Test that passing non-string message raises a TypeError."""
        with self.assertRaises(TypeError):
            encrypt(12345, 3)  # type: ignore

        with self.assertRaises(TypeError):
            decrypt(None, 3)  # type: ignore


if __name__ == "__main__":
    unittest.main()
