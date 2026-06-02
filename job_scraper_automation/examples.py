"""
Georgian Job Scraper - Quick Start Guide

This script demonstrates how to use the job scraper automation system.
"""

from job_scraper_automation.main import JobScraperOrchestrator
from job_scraper_automation.utils import LocationHelper, ContactHelper

# Example 1: Basic usage
print("=" * 80)
print("EXAMPLE 1: Basic Job Scraping")
print("=" * 80)

orchestrator = JobScraperOrchestrator()
jobs = orchestrator.run(min_match_score=0, export=True)
print(f"Found {len(jobs)} jobs total\n")

# Example 2: Filter by match score
print("=" * 80)
print("EXAMPLE 2: Filter by Resume Match Score")
print("=" * 80)

filtered_jobs = orchestrator.filter_jobs(min_match_score=50)
print(f"Found {len(filtered_jobs)} jobs with match score >= 50%\n")

# Example 3: Display job details
print("=" * 80)
print("EXAMPLE 3: Job Details")
print("=" * 80)

if jobs:
    job = jobs[0]
    print(f"Title: {job.get('title')}")
    print(f"Company: {job.get('company')}")
    print(f"Location: {job.get('location')}")
    print(f"Contact Phone: {job.get('contact_phone')}")
    print(f"Contact Email: {job.get('contact_email')}")
    print(f"Match Score: {job.get('resume_match_score')}%")
    print(f"Training Provided: {job.get('training_provided')}")
    print(f"Shift Time: {job.get('shift_time')}")
    if job.get('maps_url'):
        print(f"Maps: {job.get('maps_url')}")
    print(f"Source: {job.get('source_website')}\n")

# Example 4: Location utilities
print("=" * 80)
print("EXAMPLE 4: Location Utilities")
print("=" * 80)

location = "Tbilisi, Georgia"
coords = LocationHelper.get_coordinates(location)
print(f"Coordinates for {location}: {coords}")

maps_url = LocationHelper.get_google_maps_url(location, "Tech Park")
print(f"Maps URL: {maps_url}\n")

# Example 5: Contact validation
print("=" * 80)
print("EXAMPLE 5: Contact Validation")
print("=" * 80)

phone = "+995598123456"
email = "jobs@company.ge"

print(f"Phone {phone} valid: {ContactHelper.validate_phone(phone)}")
print(f"Email {email} valid: {ContactHelper.validate_email(email)}")
