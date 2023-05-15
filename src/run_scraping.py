import codecs
import json
import os
import sys
import django
from app.parsers import work_ua, dou_ua, djinni_co
from app.models import Language, City, Job


proj = os.path.dirname(os.path.abspath('manage.py'))

sys.path.append(proj)

os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"
django.setup()


parsers = (
    (work_ua, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou_ua, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'),
    (djinni_co, 'https://djinni.co/jobs/?primary_keyword=Python&region=UKR&location=kyiv')
)

city = City.objects.filter(slug='kiev')
jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

json_str = json.dumps(jobs, ensure_ascii=False, indent=4)

with codecs.open('src/app/parsing_results/all_jobs.json', 'w', encoding='utf-8') as file:
    file.write(json_str)
