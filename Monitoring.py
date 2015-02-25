import requests
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from lxml import html
StartDate = '16.02.2015'
EndDate = '20.02.2015'
Adress='http://www.reyestr.court.gov.ua/'
StartSearchParam={'SearchExpression':'прокуратура','CourtRegion[]':'18','CourtName[]':'166','UserCourtCode':'','ChairmanName':'','RegNumber':'','RegDateBegin': StartDate,'RegDateEnd': EndDate,'CSType[]':'4','CSType[]':'3','CSType[]':'1', 'CaseNumber':'','ImportDateBegin':'','ImportDateEnd':'','Sort':'0','PagingInfo.ItemsPerPage':'25','Liga':'false',}
StartSearch=requests.post('http://www.reyestr.court.gov.ua/',data=StartSearchParam)
SoupSearchResult=BeautifulSoup(StartSearch.text)
LinkList=[]
for link in SoupSearchResult.find_all('a'):
    LinkList.append(link.get('href'))
while (None in LinkList):
    LinkList.remove(None)
CourtLink=Adress[:-1]+LinkList[6]
Adjudication=(requests.get(CourtLink)).text
Tree=html.fromstring(Adjudication)
Text=Tree.xpath('//body/text()')
print Text
File=open('/home/nebo/Monitoring/2.html','w')
#File.write(str(Adjudication))
#SoupAdjudication=BeautifulSoup(Adjudication.text)
#SoupAdjudication.originalEncoding
#StringSoupAdjudication=str(SoupAdjudication)
