import codecs
import json
import os
import sys
from django.db import DatabaseError

# Configuring the Django environment
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from app.parsers import work_ua, dou_ua, djinni_co
from app.models import City, Language, Job

# Define the parsers and their respective URLs
parsers = (
    (work_ua, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou_ua, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'),
    (djinni_co, 'https://djinni.co/jobs/?primary_keyword=Python&region=UKR&location=kyiv')
)

# Extract "City" and "Language" objects
city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()

# Perform scraping and collect jobs and errors
jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

# Save jobs to the db
for job in jobs:
    j = Job(**job, city=city, language=language)
    try:
        j.save()
    except DatabaseError:
        pass

# ? Write jobs to JSON file
json_str = json.dumps(jobs, ensure_ascii=False, indent=4)
with codecs.open('src/app/parsing_results/all_jobs.json', 'w', encoding='utf-8') as file:
    file.write(json_str)
