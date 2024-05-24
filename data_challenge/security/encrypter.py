from cryptography.fernet import Fernet


def encrypt(messages, key_file, enc_file):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    with open(key_file, "wb") as key_file:
        key_file.write(key)

    for message in messages:
        enc_message = fernet.encrypt(message.encode())
        with open(enc_file, "a") as file:
            file.write(enc_message.decode())
            file.write("\n")
