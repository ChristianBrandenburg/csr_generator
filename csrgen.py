import logging
logging.basicConfig(level=logging.INFO)

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ec

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

logger = logging.getLogger(__name__)

def generate_rsa_key(keysize):

    valid_key_size = [512,1024,2048,4096,8192,16384]
    if keysize in valid_key_size: 

        # Generate our key
        key = rsa.generate_private_key(

            public_exponent=65537,
            key_size=keysize,
        )
        return key
    else:
        logger.warning("keysize not valid: " + str(keysize))
        

def generate_ecc_key(ecc_curve):

    valid_curve = ["secp256r1","secp384r1","secp521r1","secp224r1","secp192r1","secp256k1"]
    if ecc_curve in valid_curve:

        # Generate our key
        if ecc_curve == "secp256r1":
            curve = ec.SECP256R1()
        elif ecc_curve == "secp384r1":
            curve = ec.SECP384R1()
        elif ecc_curve == "secp521r1":
            curve = ec.SECP521R1()
        elif ecc_curve == "secp224r1":
            curve = ec.SECP224R1()
        elif ecc_curve == "secp192r1":
            curve = ec.SECP192R1()                            
        elif ecc_curve == "secp256k1":
            curve = ec.SECP256K1()    

        key = ec.generate_private_key(curve)
        return key
    else:
        logger.warning("ECC curve not valid: " + ecc_curve)


def generate_csr(key, country, state, locality, organization, common_name,san_list):

    dns_names = [x509.DNSName(san) for san in san_list]

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

    # Sign the CSR with our private key.

    ).sign(key, hashes.SHA256())

    # csr_pem = csr.public_bytes(serialization.Encoding.PEM)
    # csr_formatted = csr_pem.decode("utf-8") 

    with open(r"C:\Users\Christian\Documents\Git\csr_generator\csr.pem", "wb") as f:

        f.write(csr.public_bytes(serialization.Encoding.PEM))

key = generate_rsa_key(2048)
generate_csr(key, "DK", "Copenhagen", "Copenhagen", "blueclorp", "bluewins.net",["test.bluewins.net","test2.bluewins.net"])