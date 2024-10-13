# barr4crypt

barr4crypt is a simple rotation-based encryption tool that provides a unique way to encrypt text.

## Installation

You can install barr4crypt using pip:

```py
pip install barr4crypt
```

## Usage

Here's a quick example of how to use barr4crypt:

```python
from barr4 import encrypt, verify

# Encrypt a message
message = "Hello, World!"
rot_value = 3
encrypted = encrypt(message, rot=rot_value)
print(f"Encrypted message: {encrypted}")

string = "Hello, World!"
verify_string = verify(encrypted, string, rot=3)
print(verify_string) # Outputs: True
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
