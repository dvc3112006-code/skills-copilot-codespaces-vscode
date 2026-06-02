import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

GEORGIAN_PHONE_PATTERNS = [
    r'\+995\d{9}',
    r'0\d{9}',
    r'\+995 \d{9}',
    r'0 \d{3} \d{3} \d{3}',
]

class ContactHelper:
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        if not text:
            return None
        for pattern in GEORGIAN_PHONE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        if not text:
            return None
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        if match:
            return match.group(0)
        return None
    
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        for pattern in GEORGIAN_PHONE_PATTERNS:
            if re.fullmatch(pattern, phone):
                return True
        return False
