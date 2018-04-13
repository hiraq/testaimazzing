import requests

from decimal import Decimal
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_values(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    source = soup.find('table', 'tbl-primary').find('tbody')
    trs = source.find_all('tr')
    values = []

    for tr in trs:
        tds = tr.find_all('td')
        tds.pop(0)

        for td in tds:
            values.append(Decimal(td.get_text().replace('"', '').strip()))
    
    parsed_url = urlparse(url)
    return {
        'host': parsed_url.netloc,
        'values': values,
        'highest': max(values)
    }