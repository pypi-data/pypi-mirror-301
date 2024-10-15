from cryptography.fernet import Fernet
from DecryptUtils import DecryptUtils
import os


def encrypt_password():
    # One time Encryption key generation
    key = Fernet.generate_key()
    with open('../../Resources/KeyFiles/encrypted_key.key', 'wb') as file:
        file.write(key)

    # Read the generated encryption key to be used for creating encrypted value of sensitive data
    with open("../../Resources/KeyFiles/encrypted_key.key", "rb") as f:
        key = f.read()
    cipher_suite = Fernet(key)

    # Encrypt the sensitive data
    ciphered_client_secret = cipher_suite.encrypt(b"test")  # Replace "test" with the password to be encrypted
    print(ciphered_client_secret)

    # Write the encrypted password to a file
    with open("../../Resources/KeyFiles/srv_user_credentials.bin", "wb") as f:  # Write encrypted password to a file.
        f.write(ciphered_client_secret)

    # yaml file config example if using yaml file to configure the file paths of the encrypted data file and key
    # cryptography_key: ".python_encryption/encrypted_key.bin"
    # cryptography_files: {"svc_user_cred":".python_encryption/encrypted_cognito_basic_auth.bin",
    #                      "auth_client_id":".python_encryption/encrypted_auth_client_id.bin",
    #                      "auth_client_secret":".python_encryption/encrypted_auth_client_secret.bin"}

    cryptography_key = "../Resources/KeyFiles/encrypted_key.key"
    cryptography_files = ["../Resources/KeyFiles/srv_user_credentials.bin"]

    # Decryption of sensitive data files (multiple) during run time
    cryptography_data = [{"file": "../Resources/KeyFiles/srv_user_credentials.bin", "id": "svc_user_cred"}]
    decrypted_data = DecryptUtils.get_decrypted_data(cryptography_data, cryptography_key)
    print(decrypted_data['svc_user_cred'])

    decrypted_data = DecryptUtils.get_decrypted_file_data("../../Resources/KeyFiles/srv_user_credentials.bin", cryptography_key)
    print("Single File Value = " + decrypted_data)

    # Single encrypted value
    decrypted_data = DecryptUtils.get_decrypted_value(ciphered_client_secret, cryptography_key)
    print("Value = " + decrypted_data)


def decrypt_password(cryptography_key_path: str, ciphered_client_secret_key: str):
    print(os.getcwd())
    cryptography_key = cryptography_key_path
    ciphered_client_secret = ciphered_client_secret_key
    decrypted_data = DecryptUtils.get_decrypted_value(ciphered_client_secret, cryptography_key)
    return decrypted_data
