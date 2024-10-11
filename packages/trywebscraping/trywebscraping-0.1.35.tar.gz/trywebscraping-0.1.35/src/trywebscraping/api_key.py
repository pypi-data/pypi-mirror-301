import os
import sys
from functools import lru_cache

@lru_cache(maxsize=None)
def get_api_key():
    # First, try to get the key from environment variable
    api_key = os.environ.get("TRY_WEB_SCRAPING_KEY")
    if api_key:
        return api_key
    
    # If not found in environment, try to read from .env file
    try:
        with open('.env', 'r') as env_file:
            for line in env_file:
                if line.startswith("TRY_WEB_SCRAPING_KEY="):
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        # If .env file is not found, just pass silently
        pass
    
    # If key is not found in either place, return None
    return None

def initialize_api_key():
    api_key = get_api_key()
    if api_key is None:
        if "--no-proxy" in sys.argv:
            return
        else:
            confirm = input("No API key found. Continue without proxy? (y/n): ")
            if confirm.lower() != 'y' or confirm.lower() != 'y':
                print("To set up an API key:")
                print("1. Environment variable: 'TRY_WEB_SCRAPING_KEY'")
                print("2. .env file: TRY_WEB_SCRAPING_KEY=your_api_key")
                print("\nGet a free key: https://trywebscraping.com")
                print("Support: https://cal.com/lukelucas/customer-support")
                sys.exit(1)