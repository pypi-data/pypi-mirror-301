from .fetch import Fetch
from .browse import Browse
from .api_key import get_api_key, initialize_api_key
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import json
import base64

__all__ = ['Fetch', 'Browse', 'get_api_key', 'initialize_api_key']

_INITIALIZED = False

def run_once():
    global _INITIALIZED
    if not _INITIALIZED:
        cache_file = "try_web_scraping_cache/cache.txt"
        if not os.path.exists(cache_file):
            if not os.path.exists("try_web_scraping_cache"):
                os.makedirs("try_web_scraping_cache")
            key = b"5XY4UZ6mDStpPAHFgFVpbtwKnDGVZEXA"
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            data = {"INITIALIZED": True}
            encrypted_data = encryptor.update(json.dumps(data).encode()) + encryptor.finalize()
            
            with open(cache_file, "wb") as f:
                f.write(base64.b64encode(iv + encrypted_data))
            print("TryWebScraping: We appreciate any feedback! Chat: https://cal.com/lukelucas/what-are-you-building or email: luke.lucas@trywebscraping.com (One-time message)")
    _INITIALIZED = True

# Run the initialization function
run_once()

# Initialize the API key when the module is imported
initialize_api_key()