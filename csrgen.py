import logging

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.x509.oid import ObjectIdentifier
from cryptography.hazmat.primitives import hashes

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def generate_rsa_key(keysize):
    """Function for generating RSA keys"""

    valid_key_size = [512,1024,2048,4096,8192,16384]
    if keysize in valid_key_size:

        # Generate our key
        rsakey = rsa.generate_private_key(

            public_exponent=65537,
            key_size=keysize,
        )
        return rsakey
    else:
        logger.warning("keysize not valid: %e", str(keysize))

def generate_ecc_key(ecc_curve):
    """Function for generating ECC keys"""

    valid_curve = [256,384,521,224,192]
    if ecc_curve in valid_curve:

        # Generate our key
        if ecc_curve == 256:
            curve = ec.SECP256R1()
        elif ecc_curve == 384:
            curve = ec.SECP384R1()
        elif ecc_curve == 521:
            curve = ec.SECP521R1()
        elif ecc_curve == 224:
            curve = ec.SECP224R1()
        elif ecc_curve == 192:
            curve = ec.SECP192R1()
        ecckey = ec.generate_private_key(curve)
        return ecckey
    else:
        logger.warning("ECC curve not valid: %e", ecc_curve)


def generate_tls_csr(key, country, state, locality, organization, common_name,san_list):
    """Function generating CSRs"""

    logger.info("Generating CSR for %s", common_name)
    logger.info("SANs: %s", san_list)

    dns_names = [x509.DNSName(san) for san in san_list]

    logger.info("DNS Names: %s", dns_names)
    
    # Generate a CSR
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([

        # Provide various details about who we are.
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),

    ])).add_extension(
        x509.SubjectAlternativeName(dns_names),
        critical=False,
    ).add_extension(
        x509.ExtendedKeyUsage(
        [ObjectIdentifier("1.3.6.1.5.5.7.3.1"), # Server Auth OID
        ObjectIdentifier("1.3.6.1.5.5.7.3.2")]), # Client Auth OID
        critical=False,
    # Sign the CSR with our private key.
    ).sign(key, hashes.SHA256())

    csr_pem = csr.public_bytes(serialization.Encoding.PEM)
    csr_formatted = csr_pem.decode("utf-8")

    return csr_formatted

def select_csr(common_name,organization,locality,state,country, key_algorithm, key_size, san_list):
    """Function for generating RSA keys"""

    if key_algorithm == "RSA":
        key = generate_rsa_key(key_size)
    elif key_algorithm == "ECC":
        key = generate_ecc_key(key_size)
    else:
        key = "No key generated"
        logger.warning("No key generated")

    key_pem = key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())
    key_formatted = key_pem.decode("utf-8")

    csr = generate_tls_csr(key, country, state, locality, organization, common_name,san_list)

    return csr, key_formatted