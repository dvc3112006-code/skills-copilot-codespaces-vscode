# Job Scraper Automation

Automated job scraper for Georgian job websites with resume matching and Excel/Google Sheets export.

## Features

✅ **Multi-site Scraping**
- jobs.ge
- ssjobs.ge
- Extensible architecture for adding more websites

✅ **Resume Matching**
- Calculate match score between job description and your resume
- Fuzzy string matching for accurate results
- Skill extraction from job descriptions

✅ **Location Services**
- Google Maps integration for job locations
- Georgian city database with coordinates
- Location validation

✅ **Contact Extraction**
- Phone number extraction and validation (Georgian format support)
- Email extraction and validation
- Automatic contact info detection

✅ **Export Options**
- Excel (.xlsx) with auto-formatted columns
- Google Sheets integration
- Timestamp-based file naming

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/job-scraper-automation.git
cd job-scraper-automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Configuration

Create a `.env` file in the `job_scraper_automation/` directory:

```env
# Google Sheets Configuration
GOOGLE_SHEET_ID=your_google_sheet_id_here
GOOGLE_CREDENTIALS_JSON=credentials.json

# Scraper Configuration
SCRAPE_INTERVAL_MINUTES=60
MAX_JOBS_PER_SITE=100

# Resume Path for Matching
RESUME_PATH=./resume.txt

# Export Settings
EXPORT_TO_EXCEL=true
EXPORT_TO_SHEETS=false
OUTPUT_DIRECTORY=./exports
```

## Usage

### Basic Usage

```python
from job_scraper_automation.main import JobScraperOrchestrator

orchestrator = JobScraperOrchestrator()
jobs = orchestrator.run(min_match_score=50, export=True)
```

### Command Line

```bash
cd job_scraper_automation
python main.py
```

### Advanced Usage

```python
from job_scraper_automation.scrapers import JobsGeScraper
from job_scraper_automation.matcher import ResumeMatcher
from job_scraper_automation.exporter import JobExporter

# Custom scraping
scraper = JobsGeScraper()
jobs = scraper.scrape()

# Resume matching
matcher = ResumeMatcher('./my_resume.txt')
for job in jobs:
    score = matcher.calculate_match_score(job['description'])
    job['match_score'] = score

# Export
exporter = JobExporter('./exports')
exporter.export_to_excel(jobs, 'my_jobs.xlsx')
```

## Output Format

The exported spreadsheet includes:

| Column | Description |
|--------|-------------|
| title | Job title |
| company | Company name |
| role | Job role/position |
| location | Job location |
| contact_phone | Contact phone number |
| contact_email | Contact email address |
| training_provided | Whether training is provided |
| shift_time | Shift timing |
| resume_match_score | Match score (0-100) |
| description | Job description |
| url | Job posting URL |
| source_website | Source website |
| posted_date | Date posted |

## Resume Matching

Place your resume as plain text in `./resume.txt` or configure the path in `.env`:

```env
RESUME_PATH=./resume.txt
```

The system will calculate a match score (0-100) for each job based on similarity with your resume.

## Google Sheets Integration

To enable Google Sheets export:

1. Create a Google Sheet and get its ID
2. Set up Google Cloud credentials (Service Account)
3. Update `.env`:
```env
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_CREDENTIALS_JSON=credentials.json
EXPORT_TO_SHEETS=true
```

## Project Structure

```
job_scraper_automation/
├── scrapers/
│   ├── base_scraper.py      # Abstract base class
│   ├── jobs_ge_scraper.py   # jobs.ge implementation
│   ├── ssjobs_ge_scraper.py # ssjobs.ge implementation
│   └── __init__.py
├── matcher/
│   ├── resume_matcher.py    # Resume matching logic
│   └── __init__.py
├── exporter/
│   ├── job_exporter.py      # Excel/Sheets export
│   └── __init__.py
├── utils/
│   ├── location_helper.py   # Location utilities
│   ├── contact_helper.py    # Contact validation
│   └── __init__.py
├── main.py                  # Main orchestrator
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
└── README.md               # This file
```

## Extending with New Websites

1. Create a new scraper class in `scrapers/`:

```python
from .base_scraper import BaseScraper

class NewWebsiteScraper(BaseScraper):
    def __init__(self):
        super().__init__('https://newwebsite.ge', 'newwebsite.ge')
    
    def scrape(self):
        # Implement scraping logic
        pass
```

2. Add to main.py scrapers list:

```python
from scrapers import NewWebsiteScraper

self.scrapers = [
    JobsGeScraper(),
    SsJobsGeScraper(),
    NewWebsiteScraper(),  # Add here
]
```

## Troubleshooting

### No jobs found
- Check if websites are accessible
- Verify CSS selectors are correct (websites may update HTML)
- Check logs for error messages

### Resume matching not working
- Ensure resume file path is correct
- Verify file encoding is UTF-8

### Google Sheets export fails
- Check credentials.json is valid
- Verify GOOGLE_SHEET_ID is correct
- Ensure service account has edit access to sheet

## Logging

Logs are configured to show INFO level and above. For debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Tips

- Adjust `SCRAPE_INTERVAL_MINUTES` based on your needs
- Use `min_match_score` to filter low-relevance jobs
- Set reasonable timeouts in scrapers
- Consider using proxies for large-scale scraping

## Legal Notice

- Respect website terms of service
- Don't overload servers with frequent requests
- Check robots.txt before scraping
- Some websites may require permission for scraping

## License

MIT License - see LICENSE file

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues or questions, please create an issue on GitHub.

---

**Happy job hunting! 🚀**
