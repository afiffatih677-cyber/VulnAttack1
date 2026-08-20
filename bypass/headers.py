# bypass/headers.py
# ================================================================
# Header Manager untuk rotasi User-Agent dan header lainnya
# ================================================================

import random
import logging
from .utils import Utils

class HeaderManager:
    """Manager untuk header HTTP"""

    def __init__(self, user_agents=None, custom_headers=None):
        """
        Inisialisasi HeaderManager

        Args:
            user_agents (list): Daftar User-Agent
            custom_headers (dict): Header kustom tambahan
        """
        self.user_agents = user_agents or Utils.load_user_agents()
        self.default_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        if custom_headers:
            self.default_headers.update(custom_headers)

    def get_random_ua(self):
        """Mendapatkan User-Agent acak dari daftar"""
        if not self.user_agents:
            logging.warning("No User-Agent list available.")
            return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        return random.choice(self.user_agents)

    def get_headers(self, custom_headers=None, random_ua=True):
        """
        Mendapatkan dictionary header

        Args:
            custom_headers (dict): Header tambahan
            random_ua (bool): Jika True, gunakan User-Agent acak

        Returns:
            dict: Header dictionary
        """
        headers = self.default_headers.copy()
        if random_ua:
            headers['User-Agent'] = self.get_random_ua()
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def add_cookie(self, cookie_string):
        """
        Tambahkan cookie ke header

        Args:
            cookie_string (str): Cookie string (format: key=value; key2=value2)
        """
        self.default_headers['Cookie'] = cookie_string

    def set_referer(self, referer):
        """Set header Referer"""
        self.default_headers['Referer'] = referer

    def set_origin(self, origin):
        """Set header Origin"""
        self.default_headers['Origin'] = origin