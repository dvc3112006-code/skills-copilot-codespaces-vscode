"""
Scraper for jobs.ge website
"""
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class JobsGeScraper(BaseScraper):
    """Scraper for jobs.ge"""
    
    def __init__(self):
        super().__init__('https://jobs.ge', 'jobs.ge')
    
    def scrape(self) -> List[Dict]:
        """Scrape jobs from jobs.ge"""
        jobs = []
        
        try:
            # Main page URL - adjust based on actual site structure
            url = f"{self.base_url}/en/search"
            response = self._get_page(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings (adjust selectors based on actual HTML structure)
            job_listings = soup.find_all('div', class_='job-listing')
            
            logger.info(f"Found {len(job_listings)} job listings on jobs.ge")
            
            for listing in job_listings:
                try:
                    job = self._parse_job_listing(listing)
                    if job:
                        jobs.append(self.standardize_job(job))
                except Exception as e:
                    logger.warning(f"Error parsing job listing: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping jobs.ge: {e}")
        
        return jobs
    
    def _parse_job_listing(self, listing) -> Dict:
        """Parse individual job listing"""
        try:
            # These selectors need to be adjusted based on actual site HTML
            title = listing.find('h2', class_='job-title')
            company = listing.find('div', class_='company-name')
            location = listing.find('span', class_='job-location')
            description = listing.find('p', class_='job-description')
            
            # Extract contact info (may need to click or access detail page)
            job_url = listing.find('a', class_='job-link')
            
            job_data = {
                'title': title.text.strip() if title else '',
                'company': company.text.strip() if company else '',
                'location': location.text.strip() if location else '',
                'description': description.text.strip() if description else '',
                'url': job_url['href'] if job_url else '',
            }
            
            # Fetch detailed job page for additional info
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
            response = self._get_page(job_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            details = {}
            
            # Extract phone number
            phone_elem = soup.find('a', href=lambda x: x and 'tel:' in x)
            if phone_elem:
                details['contact_phone'] = phone_elem.text.strip()
            
            # Extract email
            email_elem = soup.find('a', href=lambda x: x and 'mailto:' in x)
            if email_elem:
                details['contact_email'] = email_elem.text.strip()
            
            # Look for training info in description
            full_text = soup.get_text().lower()
            details['training_provided'] = 'Yes' if 'training' in full_text else 'Unknown'
            
            # Look for shift time
            if 'shift' in full_text:
                details['shift_time'] = 'Multiple shifts'
            else:
                details['shift_time'] = 'Not specified'
            
            return details
            
        except Exception as e:
            logger.warning(f"Error getting job details from {job_url}: {e}")
            return {}