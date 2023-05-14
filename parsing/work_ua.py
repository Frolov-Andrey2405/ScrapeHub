import requests
# import codecs
import json
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

domain = 'https://www.work.ua'
url = 'https://www.work.ua/jobs-kyiv-python/'

resp = requests.get(url, headers=headers)

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

json_str = json.dumps(jobs, ensure_ascii=False, indent=4)

with open('parsing/web/work_ua.json', 'w', encoding='utf-8') as f:
    f.write(json_str)

# h = codecs.open('parsing/web/work_ua.json', 'w', encoding='utf-8')
# h.write(str(jobs))
# h.close()
