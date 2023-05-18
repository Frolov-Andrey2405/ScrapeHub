import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraping_service.settings')

# Configure Django settings
django.setup()

# Import the necessary modules and functions
from app.parsers import work_ua, dou_ua, djinni_co
from app.models import City, Language, Job, Error, Url
from django.contrib.auth import get_user_model

User = get_user_model()


def get_settings():
    """
    The get_settings function returns a set of tuples containing the city_id,
    language_id for each user who has send_email=True.

    The function is used to determine which users should receive an email.
    """
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)

    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []

    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)

    return urls


q = get_settings()
u = get_urls(q)


def run_scraping():
    """
    The run_scraping function is the main function of this module.
    It runs all three scraping functions and saves their results to the database.
    """
    work_ua_url = 'https://www.work.ua/jobs-kyiv-python/'
    dou_ua_url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'
    djinni_co_url = 'https://djinni.co/jobs/?primary_keyword=Python&region=UKR&location=kyiv'

    work_ua_jobs, work_ua_errors = work_ua(
        work_ua_url, city=None, language=None)
    save_jobs(work_ua_jobs)

    dou_ua_jobs, dou_ua_errors = dou_ua(dou_ua_url, city=None, language=None)
    save_jobs(dou_ua_jobs)

    djinni_co_jobs, djinni_co_errors = djinni_co(
        djinni_co_url, city=None, language=None)
    save_jobs(djinni_co_jobs)

    if work_ua_errors:
        er = Error(data=work_ua_errors)
        er.save()

    if dou_ua_errors:
        er = Error(data=dou_ua_errors)
        er.save()

    if djinni_co_errors:
        er = Error(data=djinni_co_errors)
        er.save()


def save_jobs(jobs):
    """
    The save_jobs function takes a list of dictionaries as an argument.
    Each dictionary represents a job posting, and contains the following keys:
        url - The URL of the job
        title - The title of the job
        company - The name of the company offering this position
        description - A short description about what this position entails
    """
    for job_data in jobs:
        city = City.objects.filter(slug='kiev').first()

        language = Language.objects.filter(slug='python').first()

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
