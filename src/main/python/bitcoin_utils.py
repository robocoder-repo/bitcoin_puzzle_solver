import hashlib
import ecdsa

def private_key_to_public_key(private_key: str) -> str:
    private_key_bytes = bytes.fromhex(private_key)
    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    return '04' + key.to_string().hex()

def public_key_to_address(public_key: str) -> str:
    public_key_bytes = bytes.fromhex(public_key)
    sha256_bpk = hashlib.sha256(public_key_bytes).digest()
    ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
    return hashlib.sha256(hashlib.sha256(b"\x00" + ripemd160_bpk).digest()).hexdigest()[:40]

def private_key_to_address(private_key: str) -> str:
    return public_key_to_address(private_key_to_public_key(private_key))
