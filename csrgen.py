import logging

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography import x509
from cryptography.x509.oid import NameOID, ObjectIdentifier, ExtendedKeyUsageOID
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

def select_csr(common_name,organization,locality,state,country, key_algorithm, key_size, san_list, key_usage_dict):
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

    csr = generate_csr(key, country, state, locality, organization, common_name,san_list, key_usage_dict)

    return csr, key_formatted

def generate_csr(key, country, state, locality, organization, common_name,san_list, key_usage_dict):
    """Function generating CSRs"""

    logger.info("Generating CSR for %s", common_name)
    logger.info("SANs: %s", san_list)
    dns_names = [x509.DNSName(san) for san in san_list]
    logger.info("DNS Names: %s", dns_names)

    extended_key_usage_oids = []
    if key_usage_dict['serverauth']:
        extended_key_usage_oids.append(ExtendedKeyUsageOID.SERVER_AUTH)
    if key_usage_dict['clientauth']:
        extended_key_usage_oids.append(ExtendedKeyUsageOID.CLIENT_AUTH)
    if key_usage_dict['emailprotect']:
        extended_key_usage_oids.append(ExtendedKeyUsageOID.EMAIL_PROTECTION)
    if key_usage_dict['sign']:
        extended_key_usage_oids.append(ExtendedKeyUsageOID.CODE_SIGNING)
    if key_usage_dict['timestamp']:
        extended_key_usage_oids.append(ExtendedKeyUsageOID.TIME_STAMPING)
    
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
        x509.KeyUsage(
            digital_signature = key_usage_dict["digitalsignature"], 
            content_commitment = key_usage_dict["nonrepudation"], 
            key_encipherment = key_usage_dict["keyencipher"],  
            data_encipherment = key_usage_dict["dataencipher"],  
            key_agreement = key_usage_dict["keyagree"],  
            key_cert_sign = key_usage_dict["certsign"],  
            crl_sign = key_usage_dict["crlsign"],
            encipher_only = key_usage_dict["encipher"],  
            decipher_only = key_usage_dict["decipher"]
        ),critical=True,

    ).add_extension(
        x509.ExtendedKeyUsage(extended_key_usage_oids),
        critical=False,

    # Sign the CSR with our private key.
    ).sign(key, hashes.SHA256())

    csr_pem = csr.public_bytes(serialization.Encoding.PEM)
    csr_formatted = csr_pem.decode("utf-8")

    return csr_formatted



# Key usages
# Digital signature 2.5.29.37.3
# Non-repudiation 1.0.13888.3
# Key encipherment 2.5.29.15
# Data encipherment 1.3.6.1.4.1.311.10.3.4
# Secure email 1.3.6.1.5.5.7.3.4
# Key agreement 2.5.29.15 
# Certificate signing  2.5.29.15
# CRL signing
# Encipher only
# Decipher only

# TLS Web server authentication	
# Digital signature, key encipherment or key agreement

# TLS Web client authentication
# Digital signature and/or key agreement

# Sign (downloadable) executable code
# Digital signature

# Email protection
# Digital signature, non-repudiation, and/or key encipherment or key agreement

# IPSEC End System (host or router)
# Digital signature and/or key encipherment or key agreement

# IPSEC Tunnel
# Digital signature and/or key encipherment or key agreement

# IPSEC User
# Digital signature and/or key encipherment or key agreement

# Timestamping
# Digital signature, non-repudiation. 