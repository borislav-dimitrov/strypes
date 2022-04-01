from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self):
        self._key = b"UldGNfHfPDDFdDpf-eLNx8rnoi9S-qyYEEKUI-MA3N4="

    def encrypt_pwd(self, plain):
        cipher_suite = Fernet(self._key)
        encrypted_pwd = cipher_suite.encrypt(f"{plain}".encode())
        return encrypted_pwd

    def decrypt_pwd(self, encrypted):
        cipher_suite = Fernet(self._key)
        return cipher_suite.decrypt(encrypted).decode()

    def compare(self, plain, encrypted):
        cipher_suite = Fernet(self._key)
        decoded = cipher_suite.decrypt(encrypted).decode()
        if plain == decoded:
            return True
        else:
            return False

    @staticmethod
    def check_strong_pwd(pwd: str) -> str:
        """
        Validate password
        :param pwd: password in plain text
        :return: Status: "Ok" or failed validations
        """
        specials = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                    "-", "_", "=", "+", "[", "{", "]", "}", ";", ":",
                    "'", "\"", "\\", "|", ",", "<", ".", ">", "/", "?", "`", "~"]
        validations_failed = ""
        if len(pwd) < 8:
            validations_failed += "Password must be at least 8 characters long!\n"
        if not any(char.isupper() for char in pwd):
            validations_failed += "Password should have at least one uppercase letter!\n"
        if not any(char.islower() for char in pwd):
            validations_failed += "Password should have at least one lowercase letter!\n"
        if not any(char in specials for char in pwd):
            validations_failed += "Password should contain at least one special character!"

        if validations_failed == "":
            return "Ok"
        else:
            return validations_failed.strip()
