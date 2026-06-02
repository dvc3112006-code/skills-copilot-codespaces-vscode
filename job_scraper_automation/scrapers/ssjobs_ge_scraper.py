"""
Scraper for ssjobs.ge website
"""
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class SsJobsGeScraper(BaseScraper):
    """Scraper for ssjobs.ge"""
    
    def __init__(self):
        super().__init__('https://ssjobs.ge', 'ssjobs.ge')
    
    def scrape(self) -> List[Dict]:
        """Scrape jobs from ssjobs.ge"""
        jobs = []
        
        try:
            # Main page URL
            url = f"{self.base_url}/jobs"
            response = self._get_page(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings (adjust selectors based on actual site structure)
            job_listings = soup.find_all('div', class_='job-item')
            
            logger.info(f"Found {len(job_listings)} job listings on ssjobs.ge")
            
            for listing in job_listings:
                try:
                    job = self._parse_job_listing(listing)
                    if job:
                        jobs.append(self.standardize_job(job))
                except Exception as e:
                    logger.warning(f"Error parsing job listing: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping ssjobs.ge: {e}")
        
        return jobs
    
    def _parse_job_listing(self, listing) -> Dict:
        """Parse individual job listing"""
        try:
            # These selectors need to be adjusted based on actual site HTML
            title = listing.find('h3', class_='job-title')
            company = listing.find('span', class_='company')
            location = listing.find('span', class_='location')
            
            job_link = listing.find('a', class_='job-link')
            job_url = job_link['href'] if job_link else ''
            
            job_data = {
                'title': title.text.strip() if title else '',
                'company': company.text.strip() if company else '',
                'location': location.text.strip() if location else '',
                'url': job_url,
            }
            
            # Fetch detailed job page
            if job_data['url']:
                detail_info = self._get_job_details(job_data['url'])
                job_data.update(detail_info)
            
            return job_data
            
        except Exception as e:
            logger.warning(f"Error parsing listing: {e}")
            return None
    
    def _get_job_details(self, job_url: str) -> Dict:
        """Fetch additional job details from detail page"""
        try:
            if not job_url.startswith('http'):
                job_url = self.base_url + job_url
            
            response = self._get_page(job_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            details = {}
            
            # Extract description
            desc_elem = soup.find('div', class_='job-description')
            if desc_elem:
                details['description'] = desc_elem.text.strip()
            
            # Extract contact information
            contact_elem = soup.find('div', class_='contact-info')
            if contact_elem:
                phone_link = contact_elem.find('a', href=lambda x: x and 'tel:' in x)
                if phone_link:
                    details['contact_phone'] = phone_link.text.strip()
                
                email_link = contact_elem.find('a', href=lambda x: x and 'mailto:' in x)
                if email_link:
                    details['contact_email'] = email_link.text.strip()
            
            # Extract shift information
            shift_elem = soup.find('span', class_='shift-time')
            if shift_elem:
                details['shift_time'] = shift_elem.text.strip()
            
            # Check for training
            full_text = soup.get_text().lower()
            details['training_provided'] = 'Yes' if any(word in full_text for word in ['training', 'ტრეინინგი']) else 'Unknown'
            
            return details
            
        except Exception as e:
            logger.warning(f"Error getting job details from {job_url}: {e}")
            return {}