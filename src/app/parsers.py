import requests
from bs4 import BeautifulSoup as bs
from random import randint

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
]


def work_ua(url):

    domain = 'https://www.work.ua'
    resp = requests.get(url, headers=headers[randint(0, 2)])

    jobs = []
    errors = []

    if resp.status_code == 200:
        soup = bs(resp.content, 'html.parser')
        main_div = soup.find('div', id='pjax-job-list')

        if main_div:
            div_list = main_div.find_all(
                'div', attrs={
                    'class': 'job-link'})

            for div in div_list:
                title = div.find('h2')
                href = title.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')

                if logo:
                    company = logo['alt']

                jobs.append({
                    'title': title.text,
                    'href': domain + href,
                    'description': content,
                    'company': company
                })

        else:
            errors.append({
                'url': url,
                'title': "<div> doesn't exist",
            })

    else:
        errors.append({
            'url': url,
            'title': "Page doesn't respond",
        })

    return jobs, errors


def dou_ua(url):
    resp = requests.get(url, headers=headers[randint(0, 2)])

    jobs = []
    errors = []

    if resp.status_code == 200:
        soup = bs(resp.content, 'html.parser')
        main_div = soup.find('div', id='vacancyListId')

        if main_div:
            li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})

            for li in li_list:
                if '__hot' not in li['class']:
                    title_div = li.find('div', {'class': 'title'})
                    title_a = title_div.find('a', {'class': 'vt'})
                    title = title_a.text.strip()
                    href = title_a['href']
                    company_a = title_div.find('a', {'class': 'company'})
                    company = company_a.text.split('\xa0')[-1]
                    content_div = li.find('div', {'class': 'sh-info'})
                    content = content_div.text.strip()

                    jobs.append({
                        'title': title,
                        'href': href,
                        'description': content,
                        'company': company
                    })

        else:
            errors.append({
                'url': url,
                'title': "<div> doesn't exist",
            })

    else:
        errors.append({
            'url': url,
            'title': "Page doesn't respond",
        })

    return jobs, errors


def djinni_co(url):
    resp = requests.get(url, headers=headers[randint(0, 2)])

    jobs = []
    errors = []

    if resp.status_code == 200:
        soup = bs(resp.content, 'html.parser')
        main_ul = soup.find('ul', attrs={'class': 'list-unstyled list-jobs'})

        if main_ul:
            li_list = main_ul.find_all(
                'li', attrs={'class': 'list-jobs__item list__item'})

            for li in li_list:
                title_a = li.find('a', attrs={'class': 'profile'})
                title = title_a.span.text.strip()
                href = title_a['href']

                company_a = li.find(
                    'div', attrs={'class': 'list-jobs__details__info'})
                company = company_a.a.text.strip() if company_a else 'No name'

                content_div = li.find(
                    'div', attrs={
                        'class': 'list-jobs__description position-relative'})
                content = content_div.text.strip() if content_div else ''

                jobs.append({
                    'title': title,
                    'href': href,
                    'description': content,
                    'company': company
                })

        else:
            errors.append({
                'url': url,
                'title': "<ul> doesn't exist",
            })

    else:
        errors.append({
            'url': url,
            'title': "Page doesn't respond",
        })

    return jobs, errors


__all__ = ('work_ua', 'dou_ua', 'djinni_co')

# work_ua('https://www.work.ua/jobs-kyiv-python/')
# dou_ua('https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python')
# djinni_co('https://djinni.co/jobs/?primary_keyword=Python&region=UKR&location=kyiv')
