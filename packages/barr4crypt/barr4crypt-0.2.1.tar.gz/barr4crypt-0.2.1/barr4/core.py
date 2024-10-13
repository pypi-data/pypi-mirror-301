import random
import string
import hashlib
from typing import Dict

# Constants
ALPHABET_SEC: Dict[str, str] = {
    'A': 'abcd', 'B': 'efgh', 'C': 'ijkl', 'D': 'mnop',
    'E': 'qrst', 'F': 'uvwx', 'G': 'yz',
    'a': 'ABCD', 'b': 'EFGH', 'c': 'IJKL', 'd': 'MNOP',
    'e': 'QRST', 'f': 'UVWX', 'g': 'YZ',
}

NUM_STR: Dict[int, str] = {
    i: chr(65 + i) if i < 7 else chr(97 + i - 7) for i in range(14)
}

STR_NUM: Dict[str, int] = {v: k for k, v in NUM_STR.items()}

def id_generator(size: int = 6, chars: str = string.ascii_letters + string.digits + string.punctuation) -> str:
    """Generate a random ID of specified size using the given character set."""
    return ''.join(random.choice(chars) for _ in range(size))

def check(char: str, rot: int) -> str:
    """
    Encrypt a single character using the rotation cipher.
    
    Args:
    char (str): The character to encrypt.
    rot (int): The rotation value.

    Returns:
    str: The encrypted character representation.
    """
    if not char.isalpha():
        return f"${ord(char):03d}"  # Encode special characters as $xxx where xxx is the ASCII code
    
    base = 7 if char.isupper() else 0
    for section in range(base, base + 7):
        if char in ALPHABET_SEC[NUM_STR[section]]:
            index = ALPHABET_SEC[NUM_STR[section]].index(char)
            rotated_index = (index + rot) % len(ALPHABET_SEC[NUM_STR[section]])
            rotated_section = (section + rot) % 7 + base
            return f"{NUM_STR[rotated_section]}{rotated_index:02d}"
    
    raise ValueError(f"Character '{char}' not found in the alphabet sections")

def encrypt(text: str, rot: int = 0) -> str:
    """
    Encrypt the given text using the rotation cipher and then hash the result.
    
    Args:
    text (str): The text to encrypt.
    rot (int): The rotation value (default is 0), max useful value is 27.

    Returns:
    str: The SHA-256 hash of the encrypted text.
    """

    encrypted_text = ''.join(check(char, rot) for char in text)
    return hashlib.sha256(encrypted_text.encode()).hexdigest()

def verify(encripted_text, text_to_check, rot: int = 0):
    return encripted_text == encrypt(text_to_check, rot)
