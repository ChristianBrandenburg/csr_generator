import logging

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa, ec

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def key_decode(data):

        # Extract key usage
    key_usage = data.extensions.get_extension_for_class(x509.KeyUsage).value
    key_usage_list = []
    if key_usage.digital_signature:
        key_usage_list.append("digital_signature")
    if key_usage.content_commitment:
        key_usage_list.append("content_commitment")
    if key_usage.key_encipherment:
        key_usage_list.append("key_encipherment")
    if key_usage.data_encipherment:
        key_usage_list.append("data_encipherment")
    if key_usage.key_agreement:
        key_usage_list.append("key_agreement")
        if key_usage.encipher_only:
            key_usage_list.append("encipher_only")
        if key_usage.decipher_only:
            key_usage_list.append("decipher_only")
    if key_usage.key_cert_sign:
        key_usage_list.append("key_cert_sign")
    if key_usage.crl_sign:
        key_usage_list.append("crl_sign")

    # Extract Extended Key Usage (EKU)
    eku = data.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value
    eku_list = []
    for oid in eku:
        eku_list.append(oid.dotted_string)

    # Map EKU OIDs to human-readable names
    eku_name_map = {
        "1.3.6.1.5.5.7.3.1": "Server Authentication",
        "1.3.6.1.5.5.7.3.2": "Client Authentication",
        "1.3.6.1.5.5.7.3.3": "Code Signing",
        "1.3.6.1.5.5.7.3.4": "Email Protection",
        "1.3.6.1.5.5.7.3.8": "Time Stamping",
        "1.3.6.1.5.5.7.3.9": "OCSP Signing",
        "1.3.6.1.5.5.7.3.5": "IPsec End System",
        "1.3.6.1.5.5.7.3.6": "IPsec Tunnel",
        "1.3.6.1.5.5.7.3.7": "IPsec User",
        "1.3.6.1.5.5.7.3.10": "Smart Card Logon"
        }
    # Map EKU OIDs to human-readable names, including OID if not found
    eku_names = [eku_name_map[oid] for oid in eku_list if oid in eku_name_map]

    return {
            "key_usage": key_usage_list,
            "extended_key_usage": eku_names
            }

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

    decoded_keys = key_decode(cert)
    key_usage_list = decoded_keys['key_usage']
    eku_names = decoded_keys['extended_key_usage']

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
        "key_usage": key_usage_list,
        "extended_key_usage": eku_names
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

    decoded_keys = key_decode(csr)
    key_usage_list = decoded_keys['key_usage']
    eku_names = decoded_keys['extended_key_usage']

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
        "key_usage": key_usage_list,
        "extended_key_usage": eku_names
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

