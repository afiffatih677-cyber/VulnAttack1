import time
import random
import logging
import urllib.parse

class WAFBypass:
    def __init__(self, patterns=None, max_retries=3, retry_delay=5):
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
        combined = response_text.lower()
        if response_headers:
            combined += ' ' + str(response_headers).lower()
        for pattern in self.patterns:
            if pattern.lower() in combined:
                logging.debug(f"WAF detected: {pattern}")
                return True
        return False

    def bypass_payload(self, payload, category='sqli'):
        variants = [payload]
        # Case randomization
        variants.append(''.join(random.choice([c.upper(), c.lower()]) for c in payload))
        # Whitespace bypass
        if category == 'sqli':
            variants.append(payload.replace(' ', '/**/'))
            variants.append(payload.replace(' ', '/*!*/'))
            variants.append(payload.replace(' ', '/**_**/'))
            # Double encoding
            variants.append(urllib.parse.quote(payload))
            variants.append(urllib.parse.quote(urllib.parse.quote(payload)))
        elif category == 'xss':
            variants.append(payload.replace('<', '%3C').replace('>', '%3E'))
            variants.append(payload.replace('<', '\\x3c').replace('>', '\\x3e'))
        return list(set(variants))

    def retry_on_block(self, request_func, *args, **kwargs):
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
            sleep_time = self.retry_delay + random.uniform(0, 2)
            time.sleep(sleep_time)
        return last_response