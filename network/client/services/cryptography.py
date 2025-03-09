from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from schemas.transaction import Transaction
from cryptography.hazmat.backends import default_backend
from services.key_service import generate_keys

# private_key, public_key = generate_keys()

# def sign_transaction(transaction: Transaction) -> str:

#     serialized_data = transaction.serialize()
#     signature = private_key.sign(
#         serialized_data.encode('utf-8'),
#         padding.PSS(
#             mgf=padding.MGF1(hashes.SHA256()),
#             salt_length=padding.PSS.MAX_LENGTH,
#         ),
#         hashes.SHA256(),
#     )
#     return signature.hex() 

# TODO: This solution if for tests only
# ---------------------------------------------------------------
private_key_pem = """
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCKNmrYp4DZCOCu1ehTa7a8uAhfvvppVikOPurjetzbED/N6+F1
O+gasdC4HkjOUP2F/MK6loUIlOyUQWiVGfpCoGMl22HVU6mfivFrMLoEbdpRkuvt
ZvfpP+/ZyRhojhbPsNAArfTYKnXBADO/8ezS9doapF2DKuFbSzqt0SimpwIDAQAB
AoGASLp14ufRn2NSh+27wRnvIMNedLOUJZXXKM3m4CkoyoV0bbFwBDav3kwvXpNh
EGAB6F2nQnQuMOPc0e7RT5RJ4bniZpZECPxwokesThMFU4ubQ4i5jlecT6dAVnqj
8sPPHeGi1ota3JxbYrG/XEOFHzTZEU6Hc4eWMtQe28kYHfECQQDVf6behvQzy2PI
KTZ6dBiZHWuWtQcPW1sn8Zc6QL6QUFCovxPp0y3hKP/oGksBs+dQqBAD/Ru/v6zF
RD2VQHRFAkEApboGpqp0kAWs7ytHd+CWxJQqac3SiwU+ceeAjNXA08KnOwOqXuWc
ZUzwgXrwg9Tz8dx+haWl6jxBCsSRwgv7+wJBAL8bzRtUYjQa0+7QNVvXoE0u8Keu
0+sDM83FjEEww2QbAJiMsh6UUnVCZhA1uP6FM4IXbn6jirtRsC3Er/tx/qECQQCG
FFEZOkL/2nelMGCr7fpMpIsD+s9iRiXVRbTNPIq7SHq/1iFakW3Mz0itmOdJ4VpT
zU5XlkL7lTASJCLA2a1NAkBQMkBDSuJ5ch0PkIIwyJg5hKxnuiF4E6k9BjQODgJj
Nvy/wpLzXdz8J7sztWiPU+HmwjjJ63Y10E/nCpRi6HQm
-----END RSA PRIVATE KEY-----
"""

public_key_pem = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCKNmrYp4DZCOCu1ehTa7a8uAhf
vvppVikOPurjetzbED/N6+F1O+gasdC4HkjOUP2F/MK6loUIlOyUQWiVGfpCoGMl
22HVU6mfivFrMLoEbdpRkuvtZvfpP+/ZyRhojhbPsNAArfTYKnXBADO/8ezS9doa
pF2DKuFbSzqt0SimpwIDAQAB
-----END PUBLIC KEY-----
"""

private_key = serialization.load_pem_private_key(
    private_key_pem.encode('utf-8'),
    password=None,
    backend=default_backend()
)

public_key = serialization.load_pem_public_key(
    public_key_pem.encode('utf-8'),
    backend=default_backend()
)

def sign_transaction(transaction: Transaction) -> str:
    
    # Serializuj dane transakcji
    serialized_data = transaction.serialize()
    
    # Podpisz dane transakcji
    signature = private_key.sign(
        serialized_data.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256()
    )
    
    # Zwróć podpis jako ciąg hex
    return signature.hex()

# ---------------------------------------------------------------