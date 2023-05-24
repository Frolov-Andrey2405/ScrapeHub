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
    The get_settings function returns a set of tuples containing the city_id
    and language_id for each user who has opted in to receive emails.

    The function is called by the send_email function,
    which uses it to determine which users should receive an email.

    """
    qs = User.objects.filter(send_email=True).values()
    settings_lst = {(q['city_id'], q['language_id']) for q in qs}
    return settings_lst


def get_urls(settings):
    """
    The get_urls function takes a list of tuples as an argument.

    The first element in each tuple is the city_id and
    the second element is the language_id.

    It then queries Url objects for all cities and
    languages specified in settings, returning a list of
    dictionaries with keys: 'city', 'language', and 'url_data'.
    """
    url_data = Url.objects.filter(
        city_id__in=[city_id for city_id, _ in settings],
        language_id__in=[language_id for _, language_id in settings]
    ).values()
    urls = []

    for data in url_data:
        tmp = {
            'city': data['city_id'],
            'language': data['language_id'],
            'url_data': data['url_data']
        }
        urls.append(tmp)

    return urls


class JobSaver:
    """
    The JobSaver class is responsible for saving scraped jobs into the database
    """
    @staticmethod
    def save_jobs(jobs):
        """
        The save_jobs function iterates over the scraped jobs,
        saves them in the database.

        It gets or creates a City object, a Language object,
        and then creates a Job object with those two objects as foreign keys.
        """
        # Iterate over the scraped jobs and save them in the database
        for job_data in jobs:
            # Get or create the City object
            city, _ = City.objects.get_or_create(slug='kiev')

            # Get or create the Language object
            language, _ = Language.objects.get_or_create(slug='python')

            # Create the Job object and save it
            Job.objects.get_or_create(
                url=job_data['url'],
                title=job_data['title'],
                company=job_data['company'],
                description=job_data['description'],
                city=city,
                language=language
            )


def main():
    """
    The main function is the entry point of the program.

    It calls all other functions in order to parse,
    save jobs from different websites.
    """
    settings = get_settings()
    url_lst = get_urls(settings)

    parsers = [
        (work_ua, 'work_ua'),
        (dou_ua, 'dou_ua'),
        (djinni_co, 'djinni_co'),
    ]

    job_saver = JobSaver()

    for url_data in url_lst:
        for parser, parser_name in parsers:
            # Extract the URL from the dictionary
            url = url_data['url_data'].get(parser_name)
            if url:
                jobs, errors = parser(
                    url, city=url_data['city'], language=url_data['language'])
                job_saver.save_jobs(jobs)

                if errors:
                    er = Error.objects.create(data=errors)


if __name__ == "__main__":
    main()
