import sys
import logging
import requests

try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False
    logging.warning("cloudscraper not installed. Install with: pip install cloudscraper")

class CloudflareBypass:
    def __init__(self, timeout=15, browser='chrome', platform='windows', delay=1):
        self.timeout = timeout
        self.browser = browser
        self.platform = platform
        self.delay = delay
        self.scraper = None
        self.session = requests.Session()

    def create_scraper(self):
        if not CLOUDSCRAPER_AVAILABLE:
            logging.warning("cloudscraper not available, using fallback session.")
            return self.session
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': self.browser, 'platform': self.platform, 'desktop': True},
            delay=self.delay
        )
        return self.scraper

    def request(self, url, method='GET', **kwargs):
        if not self.scraper:
            self.create_scraper()
        try:
            if hasattr(self.scraper, 'request'):
                return self.scraper.request(method, url, timeout=self.timeout, **kwargs)
            else:
                return self.session.request(method, url, timeout=self.timeout, **kwargs)
        except Exception as e:
            logging.error(f"CloudflareBypass request failed: {e}")
            try:
                return self.session.request(method, url, timeout=self.timeout, **kwargs)
            except:
                return None

    def get_session(self):
        if not self.scraper:
            self.create_scraper()
        return self.scraper

    def is_cloudflare_challenge(self, response):
        if not response:
            return False
        if response.status_code in [403, 503]:
            if 'cf-challenge' in str(response.headers).lower():
                return True
            if 'cloudflare' in response.text.lower() or 'cf-challenge' in response.text.lower():
                return True
        return False