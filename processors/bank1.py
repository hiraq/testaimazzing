import requests

from decimal import Decimal
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_values(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    trs = soup.find('table').find_all('tr')
    values = []
    i = 0

    for tr in trs:
        i += 1
        if i == 3:
            tables = tr.find_all('table')
            target_table = tables[1]    
            target_trs = target_table.find_all('tr')
            target_trs.pop(0)
            for target_tr in target_trs:
                target_tds = target_tr.find_all('td')
                del target_tds[0]
                del target_tds[-1]

                for td in target_tds:
                    values.append(Decimal(td.get_text().replace('"', '').strip()))

    parsed_url = urlparse(url)
    return {
        'host': parsed_url.netloc,
        'values': values,
        'highest': max(values)
    }