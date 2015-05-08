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
from docx import Document

#search_word = raw_input('Введіть фрагмент тексту судового рішення: ')
#start_date = raw_input('Введіть початок періоду пошуку (дд.мм.рррр): ')
#end_date = raw_input('Введіть кінець періоду пошуку (дд.мм.рррр): ')

search_word = 'прокуратура'
start_date = '01.02.2015'
end_date = '28.02.2015'


class inputs(object):
    '''Description'''
    def __init__(self, start_date, end_date, search_word = ''):
        self.url = 'http://www.reyestr.court.gov.ua/'
        self.search_word = search_word
        self.start_date = start_date
        self.end_date = end_date
        self.data = {'SearchExpression': self.search_word,
        'CourtRegion[]':'18',
        'CourtName[]':'166',
        'RegDateBegin': self.start_date,
        'RegDateEnd': self.end_date,
        'CSType[]': '2',
        'PagingInfo.ItemsPerPage':'25',
        'Liga':'false'}
        self.requisites = {'texts':[],'case_numbers':[], 'forms':[], 'dates': [], 'court_names': []}

    def __call__(self):    
        self.response = requests.post(self.url, self.data)
        if self.response.status_code != 200:
            raise RuntimeError('Got unexpected response', response)
        print 'response success'
        
        self.soup = BS(self.response.text)
        self.res_table = self.soup.find('table', id='tableresult')
        self.rows = self.res_table.findAll('tr')[1:]
        self.rel_links = [ row.find('td').a['href'] for row in self.rows ]

                
    #def savetofile(self):
        #if not isdir(self.path):
            #mkdir(self.path)
        #chdir(self.path)
        #self.path = ('./'+self.start_date+'-'+self.end_date)
        #Not Implemented



    def getall(self):
        u"""Description"""
        self.child_page = ''
        self.text = ''
        for link in self.rel_links:
            time.sleep(10)
            self.child_page = BS(requests.get(urljoin(self.url, link)).text)
            self.requisites['texts'].append(self.child_page.body.find('textarea', id='txtdepository').string)
        print 'Getall works'
        
        self.i=0
        for row in self.rows:
                self.i+=1
                self.requisites['case_numbers'].append(row.find('td', {"class" : "CaseNumber tr"+str(self.i)}))
                self.requisites['forms'].append(row.find('td', {"class" : "CSType tr"+str(self.i)}))
                self.requisites['dates'].append(row.find('td', {"class" : "RegDate tr"+str(self.i)}))
                self.requisites['court_names'].append(row.find('td', {"class" : "CourtName tr"+str(self.i)}))
        self.requisites['case_numbers'] = [str(BS(case_number.text)).decode('utf-8') for case_number in self.requisites['case_numbers']]
        self.requisites['forms'] = [str(BS(form.text)).decode('utf-8') for form in self.requisites['forms']]
        self.requisites['dates'] = [str(BS(date.text)).decode('utf-8') for date in self.requisites['dates']]
        self.requisites['court_names'] = [str(BS(court_name.text)).decode('utf-8') for court_name in self.requisites['court_names']]        


