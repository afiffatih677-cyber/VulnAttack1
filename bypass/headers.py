import random
import logging
from .utils import Utils

class HeaderManager:
    def __init__(self, user_agents=None, custom_headers=None):
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
        if not self.user_agents:
            return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        return random.choice(self.user_agents)

    def get_headers(self, custom_headers=None, random_ua=True):
        headers = self.default_headers.copy()
        if random_ua:
            headers['User-Agent'] = self.get_random_ua()
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def add_cookie(self, cookie_string):
        self.default_headers['Cookie'] = cookie_string

    def set_referer(self, referer):
        self.default_headers['Referer'] = referer

    def set_origin(self, origin):
        self.default_headers['Origin'] = origin