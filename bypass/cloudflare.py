# bypass/cloudflare.py
# ================================================================
# Cloudflare Bypass menggunakan cloudscraper
# ================================================================

import sys
import logging

# Cek ketersediaan cloudscraper
try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False
    logging.warning("cloudscraper not installed. Install with: pip install cloudscraper")

class CloudflareBypass:
    """Handler untuk melewati Cloudflare challenge"""

    def __init__(self, timeout=15, browser='chrome', platform='windows', delay=1):
        """
        Inisialisasi CloudflareBypass

        Args:
            timeout (int): Timeout request
            browser (str): Browser untuk emulasi (chrome, firefox, dll)
            platform (str): Platform (windows, linux, darwin)
            delay (int): Delay antar request
        """
        self.timeout = timeout
        self.browser = browser
        self.platform = platform
        self.delay = delay
        self.scraper = None
        self.session = None

    def create_scraper(self):
        """Membuat scraper cloudscraper"""
        if not CLOUDSCRAPER_AVAILABLE:
            raise ImportError("cloudscraper not installed. Install with: pip install cloudscraper")

        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': self.browser,
                'platform': self.platform,
                'desktop': True
            },
            delay=self.delay
        )
        return self.scraper

    def request(self, url, method='GET', **kwargs):
        """
        Kirim request dengan cloudscraper

        Args:
            url (str): Target URL
            method (str): HTTP method
            **kwargs: Parameter tambahan untuk request

        Returns:
            requests.Response atau None jika gagal
        """
        if not self.scraper:
            self.create_scraper()

        try:
            return self.scraper.request(method, url, timeout=self.timeout, **kwargs)
        except Exception as e:
            logging.error(f"CloudflareBypass request failed: {e}")
            return None

    def get_session(self):
        """Mendapatkan session cloudscraper"""
        if not self.scraper:
            self.create_scraper()
        return self.scraper

    def is_cloudflare_challenge(self, response):
        """
        Deteksi apakah response mengandung Cloudflare challenge

        Args:
            response (requests.Response): Response object

        Returns:
            bool: True jika ada Cloudflare challenge
        """
        if not response:
            return False
        # Cek status code
        if response.status_code in [403, 503]:
            # Cek header
            if 'cf-challenge' in str(response.headers).lower():
                return True
            # Cek body
            if 'cloudflare' in response.text.lower() or 'cf-challenge' in response.text.lower():
                return True
        return False