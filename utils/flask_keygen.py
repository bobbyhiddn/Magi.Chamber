import secrets

def generate_flask_key():
    # Generate a secure 32-byte (256-bit) random key and convert to hex
    return secrets.token_hex(32)

if __name__ == "__main__":
    key = generate_flask_key()
    print(f"FLASK_SECRET_KEY=\"{key}\"")