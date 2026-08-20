# bypass/utils.py
# ================================================================
# Utilitas untuk bypass modul
# ================================================================

import os
import json
import random
import time
import logging

class Utils:
    """Fungsi utilitas untuk bypass"""

    @staticmethod
    def load_user_agents(file_path='config/user_agents.txt'):
        """
        Memuat daftar User-Agent dari file

        Args:
            file_path (str): Path ke file user_agents.txt

        Returns:
            list: Daftar User-Agent
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except Exception as e:
                logging.error(f"Failed to load user_agents: {e}")

        # Default User-Agent jika file tidak ditemukan
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1'
        ]

    @staticmethod
    def load_bypass_settings(file_path='config/bypass_settings.json'):
        """
        Memuat konfigurasi bypass dari file JSON

        Args:
            file_path (str): Path ke bypass_settings.json

        Returns:
            dict: Konfigurasi bypass
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load bypass_settings: {e}")

        # Default settings
        return {
            "bypass": {
                "enabled": True,
                "cloudscraper": {
                    "use_cloudscraper": True,
                    "browser": "chrome",
                    "platform": "windows"
                },
                "delay": {
                    "min": 1,
                    "max": 3,
                    "randomize": True
                },
                "proxy": {
                    "enabled": False,
                    "file": "config/proxy.txt",
                    "rotate": True
                },
                "waf": {
                    "detection": True,
                    "retry_on_block": True,
                    "max_retries": 3,
                    "retry_delay": 5
                }
            }
        }

    @staticmethod
    def random_delay(min_delay=1, max_delay=3, randomize=True):
        """
        Menghasilkan delay acak

        Args:
            min_delay (int): Delay minimum
            max_delay (int): Delay maksimum
            randomize (bool): Jika True, gunakan acak

        Returns:
            float: Delay dalam detik
        """
        if randomize:
            return random.uniform(min_delay, max_delay)
        return min_delay

    @staticmethod
    def extract_domain(url):
        """Ekstrak domain dari URL"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc or parsed.path.split('/')[0]

    @staticmethod
    def is_valid_url(url):
        """Cek apakah URL valid"""
        import re
        pattern = re.compile(
            r'^https?://'  # http:// atau https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...atau ipv4
            r'(?::\d+)?'  # port opsional
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(pattern, url) is not None