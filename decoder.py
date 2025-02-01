import logging

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa, ec

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

data = """-----BEGIN CERTIFICATE-----
MIIDgzCCAmugAwIBAgIEdoEk2jANBgkqhkiG9w0BAQsFADBbMScwJQYDVQQDDB5SZWdlcnkgU2Vs
Zi1TaWduZWQgQ2VydGlmaWNhdGUxIzAhBgNVBAoMGlJlZ2VyeSwgaHR0cHM6Ly9yZWdlcnkuY29t
MQswCQYDVQQGEwJVQTAgFw0yNDExMTUwMDAwMDBaGA8yMTI0MTExNTIzMzczM1owRTERMA8GA1UE
AwwIdGVzdC5jb20xIzAhBgNVBAoMGlJlZ2VyeSwgaHR0cHM6Ly9yZWdlcnkuY29tMQswCQYDVQQG
EwJVQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJQ2Hyiw/MZaGsKZz9G+ptVyHSZS
cTftnM5VNbRwbiWz7XKse27v0qLu8d0tRLNrt/ozd6dYzT2OpyEn6dplxIsTGBlrG0ueT1GU8yDM
JrCiifhfWXOaYCfyXE8HkUYEvoGxWaGECgbE58Hx8k8CtMQnLWEmOdgjWwYj51BASRO2mx2w5QNs
Vc9FBj27/9DelfzeJPsdhA5DV3ifHZHkC5Iz7i+njg9FVyiNoc7K9WBtY8pzEzajMVazaYpVwyqu
BU3p5FgAkbca4jtlYhWQ5L9uvGr65LWbMf4lIo+T9RCiTfvkc9518RHhtfcaPH8CLN19zK44vVI+
qPGO8gkaAskCAwEAAaNjMGEwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMCAYYwHQYDVR0O
BBYEFNwbU2x57994Ru6zbQUjxVyxrvSoMB8GA1UdIwQYMBaAFNwbU2x57994Ru6zbQUjxVyxrvSo
MA0GCSqGSIb3DQEBCwUAA4IBAQB44bMHDRRQjh8j3VN+qGw3E44i4ov39X6XGbfuUORC9GtUsjz+
S4uVZX5vdidcq7JLC50evzkm7V3EkB3TJ36JbV9/IVuGFhXtcmeY/FfRKf/ak5px4hE/NgQKyLCw
ldoC4Kxj2r0+FMv2miiqz4YJvMabSHGdTeoCSz1KlBd/0QqjYAvl8jJKWzULFor1nCpn8QLEOaKy
wVEfmXaGKScfzOOaFlZ23GD9K/9qTNou43tlFycJ6brO8JCSeckbGTvVlXZMThzY3HxqpLuMOCnQ
m/HgFrM97diRQZFlBYdyIwq3zqpCCsEHFOQo3MPhXZvp/xHA25QMfJS5Ud56UpL8
-----END CERTIFICATE-----"""

def decode_cert(data):
    """Function for decoding X.509 certificate"""

    cert = x509.load_pem_x509_certificate(data)

    subject = cert.subject
    common_name = ""
    organization = ""
    locality = ""
    country = ""
    state = ""
    for item in subject:
        if item.oid == NameOID.COMMON_NAME:
            common_name = item.value
        if item.oid == NameOID.ORGANIZATION_NAME:
            organization = item.value
        if item.oid == NameOID.LOCALITY_NAME:
            locality = item.value
        if item.oid == NameOID.COUNTRY_NAME:
            country = item.value
        if item.oid == NameOID.STATE_OR_PROVINCE_NAME:
            state = item.value

    public_key = cert.public_key()
    if isinstance(public_key, rsa.RSAPublicKey):
        key_algorithm = "RSA"
        key_size = public_key.key_size
    elif isinstance(public_key, ec.EllipticCurvePublicKey):
        key_size = public_key.curve.key_size
        key_algorithm = "ECC"
    else:
        key_size = "Unknown"
        key_algorithm = "Unknown"

    SHA256_hash = cert.fingerprint(hashes.SHA256()).hex()
    SHA1_hash = cert.fingerprint(hashes.SHA1()).hex()
    MD5_hash = cert.fingerprint(hashes.MD5()).hex()
    serial_number = cert.serial_number

    validity_start = cert.not_valid_before.strftime("%d-%m-%Y")
    validity_end = cert.not_valid_after.strftime("%d-%m-%Y")

    return {
        "common_name": common_name,
        "organization": organization,
        "locality": locality,
        "country": country,
        "state": state,
        "key_algorithm": key_algorithm,
        "key_size": key_size,
        "SHA256_hash": SHA256_hash,
        "SHA1_hash": SHA1_hash,
        "MD5_hash": MD5_hash,
        "serial_number": serial_number,
        "validity_start": validity_start,
        "validity_end": validity_end,
    }

def decode_csr(data):
    """Function for decoding X.509 CSR"""

    csr = x509.load_pem_x509_csr(data)

    # Initialize variables for CSR subject fields
    common_name = ""
    organization = ""
    locality = ""
    country = ""
    state = ""

    # Extract subject attributes
    subject = csr.subject
    for item in subject:
        if item.oid == NameOID.COMMON_NAME:
            common_name = item.value
        elif item.oid == NameOID.ORGANIZATION_NAME:
            organization = item.value
        elif item.oid == NameOID.LOCALITY_NAME:
            locality = item.value
        elif item.oid == NameOID.COUNTRY_NAME:
            country = item.value
        elif item.oid == NameOID.STATE_OR_PROVINCE_NAME:
            state = item.value

    # Extract public key information
    public_key = csr.public_key()
    if isinstance(public_key, rsa.RSAPublicKey):
        key_algorithm = "RSA"
        key_size = public_key.key_size  # RSA key size in bits
    elif isinstance(public_key, ec.EllipticCurvePublicKey):
        key_algorithm = "ECC"
        key_size = public_key.curve.key_size  # EC key size in bits
    else:
        key_algorithm = "Unknown"
        key_size = "Unknown"

    # Return extracted details
    return {
        "common_name": common_name,
        "organization": organization,
        "locality": locality,
        "country": country,
        "state": state,
        "key_algorithm": key_algorithm,
        "key_size": key_size,
        "SHA256_hash": "",
        "SHA1_hash": "",
        "MD5_hash": "",
        "serial_number": "",
        "validity_start": "",
        "validity_end": "",
    }


def decode(data):
    """Function for decoding X.509 certificate"""
    "CSR or certificate"

    cert_bytes = data.encode('utf-8')

    if "BEGIN CERTIFICATE REQUEST" in data:
        result = decode_csr(cert_bytes)
    elif "BEGIN CERTIFICATE" in data:
        result = decode_cert(cert_bytes)
    else:
        result = None
        raise ValueError("Input data is neither a valid CSR nor a certificate.")
    return result