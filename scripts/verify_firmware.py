import sys
import os
import hashlib
import binascii
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "vendor", "embit", "src"))
from embit import ec

def verify_firmware(firmware_path, public_key_hex):
    """Verifies the firmware signature"""
    
    # Load public key
    try:
        pub = ec.PublicKey.parse(binascii.unhexlify(public_key_hex))
    except Exception as e:
        print(f"Error parsing public key: {e}")
        return False
        
    # Read firmware content
    with open(firmware_path, "rb") as f:
        firmware_data = f.read()
        
    # Calculate SHA256 matches firmware.py logic
    sha = hashlib.sha256(firmware_data).digest()
    
    # Read signature
    sig_path = firmware_path + ".sig"
    if not os.path.exists(sig_path):
        print(f"Error: Signature file not found: {sig_path}")
        return False
        
    with open(sig_path, "rb") as f:
        sig_der = f.read()
        
    # Verify
    try:
        sig = ec.Signature.parse(sig_der)
        if pub.verify(sig, sha):
            print("Usage: Signature VERIFIED! ✅")
            return True
        else:
            print("Signature INVALID! ❌")
            return False
    except Exception as e:
        print(f"Error verifying signature: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python verify_firmware.py <firmware.bin> <public_key_hex>")
        sys.exit(1)
        
    firmware_path = sys.argv[1]
    public_key_hex = sys.argv[2]
    
    if not os.path.exists(firmware_path):
        print(f"Error: Firmware file not found: {firmware_path}")
        sys.exit(1)
        
    verify_firmware(firmware_path, public_key_hex)
