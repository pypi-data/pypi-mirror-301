from cryptography.fernet import Fernet

# This is a placeholder key. In production, use a securely generated key.
ENCRYPTION_KEY = b'VGhpc0lzQVBsYWNlaG9sZGVyS2V5Rm9yRGV2ZWxvcG1lbnQ='

def encrypt_prompt(prompt):
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(prompt.encode())

def decrypt_prompt(encrypted_prompt):
    if isinstance(encrypted_prompt, str):
        # If it's not encrypted yet, just return it
        return encrypted_prompt
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(encrypted_prompt).decode()