import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraping_service.settings')

# Configure Django settings
django.setup()

# Import the necessary modules and functions
from app.parsers import work_ua, dou_ua, djinni_co
from app.models import City, Language, Job


def run_scraping():
    # Define the URLs for scraping
    work_ua_url = 'https://www.work.ua/jobs-kyiv-python/'
    dou_ua_url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'
    djinni_co_url = 'https://djinni.co/jobs/?primary_keyword=Python&region=UKR&location=kyiv'

    # Scrape data from work.ua
    work_ua_jobs, work_ua_errors = work_ua(
        work_ua_url, city=None, language=None)
    save_jobs(work_ua_jobs)

    # Scrape data from dou.ua
    dou_ua_jobs, dou_ua_errors = dou_ua(dou_ua_url, city=None, language=None)
    save_jobs(dou_ua_jobs)

    # Scrape data from djinni.co
    djinni_co_jobs, djinni_co_errors = djinni_co(
        djinni_co_url, city=None, language=None)
    save_jobs(djinni_co_jobs)


def save_jobs(jobs):
    # Iterate over the scraped jobs and save them in the database
    for job_data in jobs:

        # Get or create the City object
        city = City.objects.filter(slug='kiev').first()

        # Get or create the Language object
        language = Language.objects.filter(slug='python').first()

        # Create the Job object and save it
        Job.objects.create(
            url=job_data['url'],
            title=job_data['title'],
            company=job_data['company'],
            description=job_data['description'],
            city=city,
            language=language
        )


# Run the scraping and database storage
run_scraping()
