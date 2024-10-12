import requests

from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint

def scrape():
    '''
    Scrapes all the possible universities in the Kattis ranklist.
    '''

    def wrapped_get(url, name, domain):
        if requests.get(url).ok:
            return name, domain
        else: return None

    data = requests.get('https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json').json()

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = []
        for uni in data:
            uname = uni['name']
            for domain in uni['domains']:
                futures.append(executor.submit(wrapped_get, f'https://open.kattis.com/universities/{domain}', uname, domain))

    result = {}
    for f in as_completed(futures):
        ret = f.result()
        if ret:
            name, domain = ret
            result[domain] = name

    pprint(result)
    return result
