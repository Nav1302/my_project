from cryptography.fernet import Fernet
from password_utils import encrypt_password

# Generate key and save to file
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key","wb") as f:
        f.write(key)
    print("key saved successfully")

if __name__ == "__main__":
    #Umcommand this bacause only run first time
    #generate_key()

    encrypted = encrypt_password("root")
    print(encrypted)