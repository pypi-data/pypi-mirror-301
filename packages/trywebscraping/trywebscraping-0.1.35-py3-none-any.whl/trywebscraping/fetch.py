import time
from typing import Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from curl_cffi import requests, CurlOpt
import random

from .base_scraper import BaseScraper
from .api_key import get_api_key
from .utils import get_random_user_agent
from .browse import Browse

class Fetch(BaseScraper):
    def __init__(self, url):
        super().__init__(url)
        self.api_key = get_api_key()
        self.browse_fallback: Optional[Browse] = None

    def get_html(self) -> str:
        if self.html is None:
            self.html = self.fetch_url(self.url)
        return self.html

    def fetch_url(self, url: str) -> str:
        redirect_count = 0
        current_url = url

        while True:
            try:
                response = self.fetch_url_internal(current_url)
                if response is None:
                    print("Proxy failed, aborting request.")
                    return ""
                status_code = response.status_code

                if status_code in (301, 302, 307, 308):
                    if redirect_count >= self._MAX_REDIRECTS:
                        print(f"Max redirects ({self._MAX_REDIRECTS}) reached")
                        return response.text
                    redirect_count += 1
                    current_url = response.headers.get('Location')
                    if current_url:
                        print(f"Redirecting to: {current_url}")
                        continue
                    else:
                        print("Redirect status code received but no Location header found")
                return response.text
            except Exception as e:
                print(f"Error in fetch_url: {e}")
                raise Exception(f"Error fetching URL: {e}")

    def fetch_url_internal(self, url: str):
        parsed_url = urlparse(url)
        use_proxy = self.api_key is not None
        
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
        }

        if use_proxy:
            print("Using proxy for the connection.")
            proxy = f"http://{self._LOCAL_PROXY_HOST}:{self._LOCAL_PROXY_PORT}"
            proxy_headers = [f"Proxy-Authorization: {self.api_key}".encode()]
            curl_options = {
                CurlOpt.PROXYHEADER: proxy_headers
            }
            try:
                return requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, impersonate="chrome110", curl_options=curl_options)
            except requests.RequestsError as e:
                if e.code == 56:  # CURLE_RECV_ERROR
                    print(f"CONNECT tunnel failed. Error: {e}")
                    print("Proxy failed, aborting request.")
                    return None
                else:
                    raise
        else:
            print("No TRY_WEB_SCRAPING_KEY found in environment or .env file. Not using proxy.")
            return requests.get(url, headers=headers, impersonate="chrome110")
        
    def get_data(self) -> list[any]:
        try:
            # First, try to get data using Fetch
            data = super().get_data()
            if data:
                return data
        except Exception as e:
            print(f"Fetch query failed: {e}")

        # If Fetch fails or returns no data, fall back to Browse
        print("Falling back to headless browsing for data extraction...")
        if self.browse_fallback is None:
            self.browse_fallback = Browse(self.url)
        
        # Transfer the query information to the Browse instance
        self.browse_fallback.query_handler = self.query_handler
        return self.browse_fallback.get_data()