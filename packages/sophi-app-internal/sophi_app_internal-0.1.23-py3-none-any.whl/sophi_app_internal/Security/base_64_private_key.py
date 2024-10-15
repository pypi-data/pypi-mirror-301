from cryptography.hazmat.primitives import serialization
import base64

class base_64_private_key:
    @staticmethod
    def private_key_to_base64(private_key):
        """
        Encode the private key into Base64.

        Args:
            private_key: The private key object.

        Returns:
            str: Base64 encoded private key.
        """
        # Convert private key to bytes in PEM format
        pem_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        # Encode the PEM bytes to Base64
        base64_key = base64.b64encode(pem_bytes).decode('utf-8')
        return base64_key

    @staticmethod
    def base64_to_private_key_pem_string(base64_key):
        """
        Decode Base64 string back into a private key PEM string.

        Args:
            base64_key (str): Base64 encoded private key.

        Returns:
            str: Private key PEM string.
        """
        # Decode the Base64 string back to PEM bytes
        pem_bytes = base64.b64decode(base64_key)
        # Convert PEM bytes to a string
        pem_string = pem_bytes.decode('utf-8')
        return pem_string

