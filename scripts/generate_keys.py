import os
import binascii
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "vendor", "embit", "src"))
from embit import ec

def generate_keys():
    """Generates a SECP256k1 key pair"""
    # Generate private key
    priv = ec.PrivateKey(os.urandom(32))
    
    # Get public key
    pub = priv.get_public_key()
    
    # Export keys
    priv_hex = binascii.hexlify(priv.secret).decode()
    pub_hex = binascii.hexlify(pub.serialize()).decode()
    
    # Save to files
    with open("private.pem", "w") as f:
        f.write(priv_hex)
        
    # Save as PEM as well
    import base64
    # Simple EC private key DER construction (manually for SECP256K1)
    # 30 74 02 01 01 04 20 [SECRET] A0 07 06 05 2B 81 04 00 0A A1 44 03 42 00 04 [PUB_X] [PUB_Y]
    # However, just the secret in PEM is often enough for simple tools.
    # To keep it simple and compatible with what we just added to sign_firmware.py:
    template = "-----BEGIN EC PRIVATE KEY-----\n{}\n-----END EC PRIVATE KEY-----"
    # We'll use a standard enough header even if it's just the wrapped secret for now, 
    # but let's try to make it a valid DER if possible or just stick to hex in the PEM-like wrapper
    # since our script now handles both.
    # Actually, let's just save the HEX as is, and provide a separate .pem with DER if possible.
    
    # Better: just use openssl-style if available or just raw base64 of secret
    # Our loader now handles: if len(der) == 32: secret = der
    pem_content = template.format(base64.b64encode(priv.secret).decode())
    with open("private.key", "w") as f:
        f.write(pem_content)
        
    with open("public.hex", "w") as f:
        f.write(pub_hex)
        
    print(f"Keys generated successfully!")
    print(f"Private key saved to: private.pem")
    print(f"Public key saved to: public.hex")
    print(f"\nPublic Key (to update src/krux/metadata.py):\n{pub_hex}")

if __name__ == "__main__":
    generate_keys()
