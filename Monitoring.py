#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from os import mkdir
from os import chdir
from os.path import isdir
from os.path import isfile
import requests
from BeautifulSoup import BeautifulSoup as BS
from urlparse import urljoin

#search_word = raw_input('Введіть фрагмент тексту судового рішення: ')
#start_date = raw_input('Введіть початок періоду пошуку (дд.мм.рррр): ')
#end_date = raw_input('Введіть кінець періоду пошуку (дд.мм.рррр): ')

search_word = 'прокуратура'
start_date = '01.02.2015'
end_date = '28.02.2015'

url = 'http://www.reyestr.court.gov.ua/'
data = {'SearchExpression': search_word,
        'CourtRegion[]':'18',
        'CourtName[]':'166',
        'RegDateBegin': start_date,
        'RegDateEnd': end_date,
        'CSType[]':'1',
        'PagingInfo.ItemsPerPage':'100',
        'Liga':'false'}

response = requests.post(url, data)
if response.status_code != 200:
    raise RuntimeError('Got unexpected response', response)

soup = BS(response.text)
res_table = soup.find('table', id='tableresult')
rows = res_table.findAll('tr')[1:]
rel_links = [ row.find('td').a['href'] for row in rows ]


path = ('./'+start_date+'-'+end_date)

if not isdir(path):
    mkdir(path)
chdir(path)

for link in rel_links:
    if not isfile(link[9:]+'.html'): 
        time.sleep(2)
        child_page = BS(requests.get(urljoin(url, link)).text)
        text = child_page.body.find('textarea', id='txtdepository').string
        path = ('./'+start_date+'-'+end_date)
        with open(link[9:]+'.html', 'w') as f:
            f.write(text.encode('utf-8'))

def CaseNumbers(rows):
    u"""Бере рядки таблиці з результатами пошуку та повертає список номерів справ"""
    def GetCaseNum(rows):
        i=0
        case_numbers = []
        for row in rows:
            i+=1
            case_numbers.append(row.find('td', {"class" : "CaseNumber tr"+str(i)}))
        return case_numbers

    def GiveCaseNumbers(GetCaseNum):
        case_number=[]
        for num in GetCaseNum:
            nm = str(BS(num.text))
            case_number.append(nm)

        for num in case_number:
            num = num.decode('utf-8')
            
        return case_number

    temp_list = GetCaseNum(rows)

    return GiveCaseNumbers(temp_list)

def Forms(rows):
    u"""Бере рядки таблиці з результатами пошуку та повертає список форм судочинства"""
    def GetForms(rows):
        i=0
        form_list = []
        for row in rows:
            i+=1
            form_list.append(row.find('td', {"class" : "CSType tr"+str(i)}))
        return form_list

    def GiveForms(GetForms):
        form_list=[]

        for form in GetForms:
            nm = (str(BS(form.text)))
            form_list.append(nm)
        
        for form in form_list:
            form = form.decode('utf-8')

        return form_list
    temp_list = GetForms(rows)

    return GiveForms(temp_list)










