from cryptography.fernet import Fernet


def decrypt(key_file, enc_file):
    result = []
    with open(key_file, "r") as key_file:
        key = key_file.read()
    fernet = Fernet(key)
    with open(enc_file, "r") as enc_file:
        for enc_line in enc_file:
            enc_line = enc_line.strip()
            if enc_line != "":
                decrypted_value = fernet.decrypt(enc_line)
                result.append(decrypted_value.decode())
    return result
