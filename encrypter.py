import os
from cryptography.fernet import Fernet

# Get the unique_id from the user model
unique_id = "unique_id"

# Generate the key
key = Fernet.generate_key()

# Encrypt the unique_id using the key
fernet = Fernet(key)
encrypted_id = fernet.encrypt(unique_id.encode())

# Store the key and encrypted data in a text file
with open('keys.txt', 'wb') as file:
    file.write(key)
    file.write(b'\n')
    file.write(encrypted_id)