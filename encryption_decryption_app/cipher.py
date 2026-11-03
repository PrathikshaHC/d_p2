"""
Caesar Cipher Implementation
Cyber Security Project 2 - Basic Encryption & Decryption

This module provides core encryption and decryption functions using the Caesar cipher algorithm.
The Caesar cipher is a symmetric key substitution cipher where each letter in the plaintext
is shifted by a fixed number of positions down the alphabet.

IMPORTANT EDUCATIONAL DISCLAIMER:
The Caesar cipher is an ancient, basic cryptographic technique intended solely for educational
demonstration. With only 25 possible meaningful shift keys, it is vulnerable to brute-force
frequency analysis and does NOT provide secure protection for sensitive or production data.
"""

from typing import Union


def normalize_shift(shift: Union[int, float, str]) -> int:
    """
    Normalizes and validates the shift key to an integer modulo 26.
    
    Args:
        shift: The shift value provided (can be int or string representation of int).
        
    Returns:
        int: Normalized shift between 0 and 25.
        
    Raises:
        ValueError: If shift cannot be parsed as an integer.
    """
    try:
        # Check if float has non-zero fractional part
        if isinstance(shift, float):
            if not shift.is_integer():
                raise ValueError("Shift key must be an integer, not a decimal number.")
            shift = int(shift)
        else:
            shift = int(shift)
    except (ValueError, TypeError) as err:
        raise ValueError(f"Invalid shift key '{shift}'. The shift key must be a valid integer.") from err

    # Modulo 26 normalizes positive, negative, and large integers
    # Python's modulo operator (%) always returns a non-negative result in [0, 25]
    return shift % 26


def encrypt(text: str, shift: Union[int, float, str]) -> str:
    """
    Encrypts a plaintext string using the Caesar cipher with a specified shift key.
    
    Rules:
    - Uppercase letters (A-Z) are shifted and wrapped within A-Z.
    - Lowercase letters (a-z) are shifted and wrapped within a-z.
    - Spaces, numbers, and special characters/punctuation are preserved unchanged.
    - Shift is normalized using modulo 26.
    
    Mathematical formula:
    E(x) = (x + k) mod 26
    
    Args:
        text (str): The plaintext message to encrypt.
        shift (int): Number of positions to shift characters.
        
    Returns:
        str: The resulting ciphertext.
    """
    if not isinstance(text, str):
        raise TypeError("Input message must be a string.")
        
    if not text:
        return ""

    k = normalize_shift(shift)
    encrypted_chars = []

    for char in text:
        if 'A' <= char <= 'Z':
            # Shift uppercase letter within 0..25 and convert back to ASCII
            shifted_char = chr((ord(char) - ord('A') + k) % 26 + ord('A'))
            encrypted_chars.append(shifted_char)
        elif 'a' <= char <= 'z':
            # Shift lowercase letter within 0..25 and convert back to ASCII
            shifted_char = chr((ord(char) - ord('a') + k) % 26 + ord('a'))
            encrypted_chars.append(shifted_char)
        else:
            # Non-alphabetic character (numbers, punctuation, whitespace, emojis)
            encrypted_chars.append(char)

    return "".join(encrypted_chars)


def decrypt(ciphertext: str, shift: Union[int, float, str]) -> str:
    """
    Decrypts a ciphertext string produced by the Caesar cipher using the original shift key.
    
    Decryption reverses the encryption shift:
    D(x) = (x - k) mod 26
    
    Args:
        ciphertext (str): The encrypted message to decrypt.
        shift (int): The shift key that was originally used for encryption.
        
    Returns:
        str: The recovered plaintext message.
    """
    if not isinstance(ciphertext, str):
        raise TypeError("Ciphertext message must be a string.")

    if not ciphertext:
        return ""

    k = normalize_shift(shift)
    decrypted_chars = []

    for char in ciphertext:
        if 'A' <= char <= 'Z':
            # Reverse shift uppercase letter within 0..25
            reversed_char = chr((ord(char) - ord('A') - k) % 26 + ord('A'))
            decrypted_chars.append(reversed_char)
        elif 'a' <= char <= 'z':
            # Reverse shift lowercase letter within 0..25
            reversed_char = chr((ord(char) - ord('a') - k) % 26 + ord('a'))
            decrypted_chars.append(reversed_char)
        else:
            # Preserve non-alphabetic character unchanged
            decrypted_chars.append(char)

    return "".join(decrypted_chars)
