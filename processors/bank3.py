import requests

from decimal import Decimal
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_values(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', cellpadding=4)
    trs = table.find_all('tr')
    target_trs = [trs[3], trs[4], trs[5], trs[6]]
    values = []

    for tr in target_trs:
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