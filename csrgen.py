from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ec

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

def generate_rsa_key(keysize):

    # Generate our key
    key = rsa.generate_private_key(

        public_exponent=65537,
        key_size=keysize,
    )
    return key

def generate_ecc_key(ecc_curve):

    # Generate our key

    if ecc_curve == 256:
        curve = ec.SECP256R1()
    if ecc_curve == 256:
        curve = ec.SECP256R1()
    if ecc_curve == 256:
        curve = ec.SECP256R1()
    if ecc_curve == 256:
        curve = ec.SECP256R1()
    if ecc_curve == 256:
        curve = ec.SECP256R1()                            
    

    key = ec.generate_private_key(

    curve,
    )
    return key

def generate_csr(key):

    # Generate a CSR
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([

        # Provide various details about who we are.
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),

    ])).add_extension(
        x509.SubjectAlternativeName([

            # Describe what sites we want this certificate for.
            x509.DNSName(u"mysite.com"),
            x509.DNSName(u"www.mysite.com"),
            x509.DNSName(u"subdomain.mysite.com"),

        ]),

        critical=False,

    # Sign the CSR with our private key.

    ).sign(key, hashes.SHA256())

    with open(r"C:\Users\Christian\Documents\Git\csr_generator\csr.pem", "wb") as f:

        f.write(csr.public_bytes(serialization.Encoding.PEM))

key = generate_ecc_key(256)
generate_csr(key)