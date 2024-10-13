# Rotocrypt

Rotocrypt is a simple rotation-based encryption tool that provides a unique way to encrypt text.

## Installation

You can install Rotocrypt using pip:

```py
pip install rotocrypt
```

## Usage

Here's a quick example of how to use Rotocrypt:

```python
from rotocrypt import encrypt, id_generator

# Generate a random ID
random_id = id_generator(10)
print(f"Random ID: {random_id}")

# Encrypt a message
message = "Hello, World!"
rot_value = 3
encrypted = encrypt(message, rot=rot_value)
print(f"Encrypted message: {encrypted}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
