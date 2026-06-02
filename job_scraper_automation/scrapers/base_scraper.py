"""
Base scraper class for job websites
"""
import requests
from abc import ABC, abstractmethod
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for job scrapers"""
    
    def __init__(self, base_url: str, name: str):
        self.base_url = base_url
        self.name = name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Scrape job listings from the website
        
        Returns:
            List of job dictionaries with standardized fields
        """
        pass
    
    def _get_page(self, url: str, **kwargs) -> requests.Response:
        """Fetch a page with error handling"""
        try:
            response = self.session.get(url, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            raise
    
    def standardize_job(self, job_data: Dict) -> Dict:
        """
        Standardize job data to common format
        
        Required fields:
        - title: Job title
        - role: Job role/position
        - company: Company name
        - location: Job location
        - contact_phone: Contact phone number
        - contact_email: Contact email
        - training_provided: Whether training is provided (True/False/Unknown)
        - shift_time: Shift timing (e.g., "9AM-5PM", "24-hour")
        - description: Job description
        - url: Source URL
        - posted_date: Date posted
        """
        return {
            'title': job_data.get('title', ''),
            'role': job_data.get('role', ''),
            'company': job_data.get('company', ''),
            'location': job_data.get('location', ''),
            'contact_phone': job_data.get('contact_phone', ''),
            'contact_email': job_data.get('contact_email', ''),
            'training_provided': job_data.get('training_provided', 'Unknown'),
            'shift_time': job_data.get('shift_time', 'Not specified'),
            'description': job_data.get('description', ''),
            'url': job_data.get('url', ''),
            'posted_date': job_data.get('posted_date', ''),
            'source_website': self.name
        }