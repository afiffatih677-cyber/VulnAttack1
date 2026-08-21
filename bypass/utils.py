import os
import json
import random
import logging

class Utils:
    @staticmethod
    def load_user_agents(file_path='config/user_agents.txt'):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except:
                pass
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15'
        ]

    @staticmethod
    def load_bypass_settings(file_path='config/bypass_settings.json'):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "bypass": {
                "enabled": True,
                "cloudscraper": {"use_cloudscraper": True, "browser": "chrome", "platform": "windows"},
                "delay": {"min": 1, "max": 3, "randomize": True},
                "waf": {"detection": True, "retry_on_block": True, "max_retries": 3, "retry_delay": 5}
            }
        }

    @staticmethod
    def random_delay(min_delay=1, max_delay=3, randomize=True):
        return random.uniform(min_delay, max_delay) if randomize else min_delay