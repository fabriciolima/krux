import sys
import os
import hashlib
import binascii
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "vendor", "embit", "src"))
from embit import ec

def sign_firmware(firmware_path, private_key_path):
    """Signs the firmware with the given private key"""
    
    # Load private key
    with open(private_key_path, "r") as f:
        priv_content = f.read().strip()
        
    if "-----BEGIN" in priv_content:
        # Handle PEM format
        import base64
        lines = [line.strip() for line in priv_content.splitlines() 
                 if not line.startswith("-----") and line.strip()]
        pem_b64 = "".join(lines)
        der = base64.b64decode(pem_b64)
        
        # MicroPython embit 0.3.x+ ec.PrivateKey.parse expects DER or raw bytes
        # In this desktop context, we need to extract the raw secret from DER
        # A simple Secp256k1 DER private key usually has the 32-byte secret at specific offsets
        # But embit's ec.PrivateKey frequently expects just the 32-byte secret if not using .parse
        
        if len(der) == 32:
            secret = der
        elif len(der) > 32:
            # Simple DER parsing for EC Private Key (RFC 5915)
            # Typically: Sequence -> Version(1) -> Octet String (Secret)
            # Version 1 is 02 01 01
            # Octet String header for 32 bytes is 04 20
            try:
                v_idx = der.find(b"\x02\x01\x01")
                if v_idx != -1:
                    s_idx = der.find(b"\x04\x20", v_idx)
                    if s_idx != -1:
                        secret = der[s_idx+2:s_idx+34]
                    else:
                        raise ValueError("Could not find secret in DER.")
                else:
                    raise ValueError("Unsupported EC private key version.")
            except Exception as e:
                 raise ValueError(f"Could not parse PEM file: {e}")
        else:
            raise ValueError("Invalid key length.")
    else:
        # Handle Hex format
        secret = binascii.unhexlify(priv_content)
        
    priv = ec.PrivateKey(secret)
        
    # Read firmware content
    with open(firmware_path, "rb") as f:
        firmware_data = f.read()
        
    # Calculate SHA256 matches firmware.py logic
    # Firmware hash includes the size header if passed, but here we sign the file as is?
    # Checking firmware.py: sha256(firmware_filename) does NOT include header unless firmware_size is passed.
    # But verifying: firmware_hash = sha256(firmware_path) -> reads file chunks.
    # So we just hash the file content.
    
    sha = hashlib.sha256(firmware_data).digest()
    
    # Sign
    sig = priv.sign(sha)
    sig_der = sig.serialize()
    
    # Save signature
    sig_path = firmware_path + ".sig"
    with open(sig_path, "wb") as f:
        f.write(sig_der)
        
    print(f"Firmware signed successfully!")
    print(f"Signature saved to: {sig_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sign_firmware.py <firmware.bin> <private_key_file>")
        sys.exit(1)
        
    firmware_path = sys.argv[1]
    private_key_path = sys.argv[2]
    
    if not os.path.exists(firmware_path):
        print(f"Error: Firmware file not found: {firmware_path}")
        sys.exit(1)
        
    if not os.path.exists(private_key_path):
        print(f"Error: Private key file not found: {private_key_path}")
        sys.exit(1)
        
    sign_firmware(firmware_path, private_key_path)
