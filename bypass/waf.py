# bypass/waf.py
# ================================================================
# WAF Detection & Bypass
# ================================================================

import time
import random
import re
import logging

class WAFBypass:
    """Handler untuk mendeteksi dan melewati WAF"""

    def __init__(self, patterns=None, max_retries=3, retry_delay=5):
        """
        Inisialisasi WAFBypass

        Args:
            patterns (list): Daftar pattern untuk deteksi WAF
            max_retries (int): Maksimum percobaan ulang
            retry_delay (int): Delay antar percobaan (detik)
        """
        self.patterns = patterns or [
            'cloudflare', 'cf-challenge', 'captcha', 'security check',
            'access denied', 'blocked', 'mod_security', 'WAF',
            'AWS WAF', 'Imperva', 'Akamai', 'Fastly',
            '403 Forbidden', '503 Service Unavailable',
            'your request has been blocked', 'malicious activity'
        ]
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def detect(self, response_text, response_headers):
        """
        Deteksi apakah ada WAF/Cloudflare berdasarkan response

        Args:
            response_text (str): Response body
            response_headers (dict): Response headers

        Returns:
            bool: True jika terdeteksi WAF
        """
        combined = response_text.lower()
        # Tambahkan header ke deteksi
        if response_headers:
            combined += ' ' + str(response_headers).lower()

        for pattern in self.patterns:
            if pattern.lower() in combined:
                logging.debug(f"WAF detected: {pattern}")
                return True
        return False

    def retry_on_block(self, request_func, *args, **kwargs):
        """
        Coba ulang request jika terdeteksi WAF

        Args:
            request_func (function): Fungsi yang dipanggil untuk request
            *args, **kwargs: Argumen untuk request_func

        Returns:
            Response atau None jika gagal setelah retry
        """
        last_response = None
        for attempt in range(self.max_retries):
            response = request_func(*args, **kwargs)
            if response:
                if not self.detect(response.text, response.headers):
                    return response
                last_response = response
                logging.warning(f"Blocked by WAF (attempt {attempt+1}/{self.max_retries})")
            else:
                logging.warning(f"Request failed (attempt {attempt+1}/{self.max_retries})")

            # Delay dengan random untuk menghindari pola
            sleep_time = self.retry_delay + random.uniform(0, 2)
            time.sleep(sleep_time)

        return last_response