import benedict
from cryptography.fernet import Fernet


class DecryptUtils(object):
    """
       Returns Dict object of keys and decrypted values pair for the Dict object of keys and file names containing
       encrypted data passed as input parameter
       :param cryptography_data - Dict object of keys and encrypted file names
       :param cryptography_key_filename - string containing the filename of the encryption key to be used for decryption
       :return the Dict object of key and decrypted value pair
       """
    @staticmethod
    def get_decrypted_data(cryptography_data: object, cryptography_key_filename: str):

        with open(cryptography_key_filename, "rb") as f:
            for line in f:
                key = line
        cipher_suite = Fernet(key)
        decrypted_data = {}
        for cryptFiles in cryptography_data:
            cryptoDict = benedict(cryptFiles)
            with open(cryptoDict['file'], "rb") as f:
                for line in f:
                    encrypted_data = line
            decrypted_binary = cipher_suite.decrypt(encrypted_data)  # Decrypt binary encrypted file.
            decrypted_value = bytes(decrypted_binary).decode("utf-8")
            decrypted_data[cryptoDict['id']] = decrypted_value
        return decrypted_data

    """
       Returns decrypted value of the encrypted data present in the file passed as input parameter
       :param encrypted_filename - file name containing the encrypted data
       :param cryptography_key_filename - string containing the filename of the encryption key to be used for decryption
       :return the string of decrypted value
       """
    @staticmethod
    def get_decrypted_file_data(encrypted_filename: str, cryptography_key_filename: str):

        with open(cryptography_key_filename, "rb") as f:
            for line in f:
                key = line
        cipher_suite = Fernet(key)
        with open(encrypted_filename, "rb") as f:
            for line in f:
                encrypted_data = line
        decrypted_binary = cipher_suite.decrypt(encrypted_data)  # Decrypt binary encrypted file.
        decrypted_value = bytes(decrypted_binary).decode("utf-8")
        return decrypted_value

    """
       Returns decrypted value of the encrypted data passed as input parameter
       :param encrypted_data_value - encrypted data
       :param cryptography_key_filename - string containing the filename of the encryption key to be used for decryption
       :return the string of decrypted value
       """
    @staticmethod
    def get_decrypted_value(encrypted_data_value: str, cryptography_key_filename: str):

        with open(cryptography_key_filename, "rb") as f:
            for line in f:
                key = line
        cipher_suite = Fernet(key)
        decrypted_binary = cipher_suite.decrypt(encrypted_data_value)  # Decrypt binary value.
        decrypted_value = bytes(decrypted_binary).decode("utf-8")
        return decrypted_value
