import requests
import time
import random
import logging
from datetime import datetime


class BaseSpider:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def fetch_html(self, url, retry=3):
        for i in range(retry):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except Exception as e:
                self.logger.warning(f"«Î«Û ß∞‹ {url}, ÷ÿ ‘ {i+1}/{retry}: {e}")
                time.sleep(random.uniform(1, 3))
        return None
    
    def parse_datetime(self, date_str):
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d'
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except Exception:
                continue
        return datetime.now()