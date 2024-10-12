# cert_utils.py

import os
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from datetime import datetime, timezone


def extract_common_name(subject):
    """Extracts the Common Name (CN) from the subject."""
    for attribute in subject:
        if attribute.oid == x509.NameOID.COMMON_NAME:
            return attribute.value
    return None


def extract_san_extension(certificate):
    """Extracts the Subject Alternative Names (SAN) from the certificate."""
    try:
        san_extension = certificate.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        san_names = san_extension.value
        return [str(name) for name in san_names]
    except x509.ExtensionNotFound:
        return None


def decrypt_and_save_private_key(file_path, passphrase, output_path):
    """Decrypts an encrypted private key and saves it as an unencrypted PEM file."""
    with open(file_path, 'rb') as key_file:
        key_data = key_file.read()

    try:
        # Try to load the private key with the passphrase
        private_key = load_pem_private_key(key_data, password=passphrase, backend=default_backend())

        # Serialize the private key to PEM format without encryption
        unencrypted_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()  # No encryption
        )

        # Save the unencrypted private key to a file
        with open(output_path, 'wb') as output_file:
            output_file.write(unencrypted_key_pem)

        print(f"Decrypted and saved private key to {output_path}")

    except ValueError:
        print(f"Failed to decrypt the private key from {file_path}. Incorrect passphrase or invalid key.")
    except Exception as e:
        print(f"An error occurred while decrypting or saving the private key: {e}")


def process_certificate(input_data, passphrase=None):
    """Reads and processes a certificate or key from a file path or PEM-encoded string."""
    # Determine if the input is a file path or a PEM-encoded string
    if isinstance(input_data, str):
        if os.path.isfile(input_data):
            with open(input_data, 'rb') as file:
                data = file.read()
            file_path = input_data
        else:
            # Assume input_data is a PEM-encoded string
            data = input_data.encode()
            file_path = None
    else:
        raise ValueError("Input data must be a file path or a PEM-encoded string.")

    # Try to load it as a private key without a passphrase
    try:
        private_key = load_pem_private_key(data, password=None, backend=default_backend())
        print(f"{file_path if file_path else 'Input data'} is an unencrypted private key.")

        private_key_details = {
            "file_path": file_path,
            "is_valid": True,
            "type": type(private_key).__name__,
            "key_size": private_key.key_size,
        }
        return private_key_details
    except (ValueError, TypeError):
        pass

    # Try to load it as an encrypted private key
    if passphrase:
        try:
            private_key = load_pem_private_key(data, password=passphrase, backend=default_backend())
            print(f"{file_path if file_path else 'Input data'} is an encrypted private key.")

            if file_path:
                # Decrypt and save the private key
                output_path = os.path.join(os.path.dirname(file_path), '_unencrypted_key.pem')
                decrypt_and_save_private_key(file_path, passphrase, output_path)

            return private_key
        except (ValueError, TypeError):
            pass

    # Try to load it as a public key
    try:
        public_key = load_pem_public_key(data, backend=default_backend())
        print(f"{file_path if file_path else 'Input data'} is a public key.")
        return public_key
    except ValueError:
        pass

    # Try to load it as an X.509 certificate
    try:
        certificate = x509.load_pem_x509_certificate(data, default_backend())

        # Use timezone-aware properties
        valid_from = certificate.not_valid_before_utc
        valid_until = certificate.not_valid_after_utc

        # Convert 'today' to an aware datetime object in UTC
        today = datetime.now(timezone.utc)

        # Check if the certificate is valid today
        is_valid_today = valid_from <= today <= valid_until

        # Calculate the lifetime of the certificate in days
        lifetime_days = (valid_until - today).days

        details = {
            "file_path": file_path,
            "serial_number": format(certificate.serial_number, 'X'),
            "is_valid": is_valid_today,
            "issuer": certificate.issuer.rfc4514_string(),
            "subject": certificate.subject.rfc4514_string(),
            "common_name": extract_common_name(certificate.subject),
            "valid_from": valid_from.strftime('%Y-%b'),
            "valid_until": valid_until.strftime('%Y-%b'),
            "lifetime_days": lifetime_days,
        }

        # Extract SAN extension
        san_names = extract_san_extension(certificate)
        details["sans"] = san_names if san_names else None

        # Extract the public key from the certificate
        public_key_pem = certificate.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        details["public_key"] = public_key_pem

        return details

    except ValueError:
        pass

    print(f"{file_path if file_path else 'Input data'} is not a valid certificate or key.")


def find_cert_and_key_files(base_path):
    """Finds the certificate and key files in the base path."""
    cert_file_path = None
    key_file_path = None

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".crt") or file.endswith(".pem") and "cert" in file.lower():
                cert_file_path = os.path.join(root, file)
            # elif file.endswith(".key"):
            #     key_file_path = os.path.join(root, file)
            elif file == "_unencrypted_key.pem":
                key_file_path = os.path.join(root, file)

    return cert_file_path, key_file_path


def process_certificate_and_key(cert_file_path, key_file_path, passphrase=None):
    """Verifies if the private key matches the certificate."""
    with open(cert_file_path, 'rb') as cert_file:
        cert_data = cert_file.read()

    with open(key_file_path, 'rb') as key_file:
        key_data = key_file.read()

    # Load the certificate
    certificate = x509.load_pem_x509_certificate(cert_data, default_backend())

    # Extract the public key from the certificate
    cert_public_key = certificate.public_key()

    try:
        # Determine if the key is encrypted or not
        if passphrase:
            try:
                private_key = load_pem_private_key(key_data, password=passphrase, backend=default_backend())
            except TypeError:
                print("Provided passphrase, but the key is not encrypted. Loading key without passphrase.")
                private_key = load_pem_private_key(key_data, password=None, backend=default_backend())
        else:
            private_key = load_pem_private_key(key_data, password=None, backend=default_backend())

        # Compare the public key from the certificate with the public key derived from the private key
        if compare_public_keys(cert_public_key, private_key):
            print("The private key and the certificate match.")
        else:
            print("The private key and the certificate do not match.")

    except ValueError as e:
        print(f"An error occurred while loading the private key: {e}")


def get_public_key_from_private_key(private_key):
    """Extracts the public key from the given private key."""
    return private_key.public_key()


def compare_public_keys(cert_public_key, key_private_key):
    """Compares the public key from the certificate with the public key derived from the private key."""
    cert_public_key_pem = cert_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    key_public_key = get_public_key_from_private_key(key_private_key)
    key_public_key_pem = key_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return cert_public_key_pem == key_public_key_pem
