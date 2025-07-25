from cryptography.fernet import Fernet

class fakeStr(str):
    def __str__(self):
        return "********"
    def __repr__(self):
        return "********"


def load_key():
    return open("secret.key","rb").read()


def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(password.encode())

# decrypt password and return the protected string
def decrypt_password(encrypt_password):
    key = load_key()
    f = Fernet(key)
    decrypted = f.decrypt(encrypt_password).decode()
    return fakeStr(decrypted)


# final method to call from app

def get_decrypted_password():
    encrypt_password = b'gAAAAABofdheji1yleM3dZ-ff3MZkLfbopjzPkRSQzeWwlvmWLXM9HifAMLIxiBR8GNcT2q6j6VGj5TZRi2t74cBr_h48yOWIw=='
    return decrypt_password(encrypt_password)