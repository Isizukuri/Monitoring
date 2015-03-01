#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from os import mkdir as mkdir
from os import chdir as chdir
import requests
from BeautifulSoup import BeautifulSoup as BS
from urlparse import urljoin

start_date = '16.02.2015'
end_date = '20.02.2015'

url = 'http://www.reyestr.court.gov.ua/'
data = {'SearchExpression': 'прокуратура',
        'CourtRegion[]':'18',
        'CourtName[]':'166',
        'RegDateBegin': start_date,
        'RegDateEnd': end_date,
        'CSType[]':'1',
        'PagingInfo.ItemsPerPage':'50',
        'Liga':'false'}

response = requests.post(url, data)
if response.status_code != 200:
    raise RuntimeError('Got unexpected response', response)

soup = BS(response.text)
res_table = soup.find('table', id='tableresult')
rows = res_table.findAll('tr')[1:]
rel_links = [ row.find('td').a['href'] for row in rows ]

path = ('./'+start_date+'-'+end_date)
mkdir(path)
chdir(path)

for link in rel_links:
    time.sleep(2)
    path = ('./'+start_date+'-'+end_date)
    child_page = BS(requests.get(urljoin(url, link)).text)
    text = child_page.body.find('textarea', id='txtdepository').string # contents[0]
    soup_text = BS(text)
    with open(link[9:]+'.html', 'w') as f:
        f.write(text.encode('utf-8'))
