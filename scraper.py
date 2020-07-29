import requests
import json
from bs4 import BeautifulSoup

page =1
URL = 'https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/bscSrch?q.srchNm=&q.stts=0007&p='+ str(page)
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
tb =soup.find( class_='table table-bordered wb-tables table-striped')

#have the url for the next page fro the specific charity
for data in tb.find_all('tr'):
    name = data.find('a',href=True).get_text("href")
    link = "https://apps.cra-arc.gc.ca"+data.find('a',href=True)["href"]

#have the location and the date the started in temparr
for data in tb.find_all('td'):
    province = data.find('div',class_="mrgn-tp-sm")
    temparr=str(province).split()
    temparr=temparr[2:]
    temparr=temparr[:-1]
    temparr=",".join(temparr)

print(name,"\n",link,"\n",temparr,"\n")
"""
    additional data for the charity
    Registration Number
    website 
    data as of date
    description
    Revenue 
    Expense
"""
tLink = link
page = requests.get(tLink)

soup = BeautifulSoup(page.content, 'html.parser')
tb =soup.find( class_='col-md-9 col-md-push-3')

counter=0
for data in tb.find_all('strong'):
    counter+=1
    if(counter == 1):
        temparr=(data.text).split()
        temparr="".join(temparr)
        charityRegNo= (temparr)
    arr = data.find('a',href=True)
    if arr:
        charityWebsite=(arr["href"])
        break

counter=0
for data in tb.find_all('h2'):
    counter+=1
    if counter ==2:
        dateAsOf=data.text[25:]

p =soup.find(id='ongoingprograms').text
temparr=(p).split()
temparr=" ".join(temparr)[18:]
description = temparr

# expenses and revenue TODO complete this :)
for data in soup.find_all('table'):
    for d in data.find_all('th'):
        re=(d.text)

#total revenue and expenses
p = soup.find_all(class_="h5 mrgn-lft-md mrgn-tp-md")
counter=0
for data in p:
    counter+=1
    if counter ==1:
        totalRevenue= data.text[data.text.find('$'):]
    elif counter ==2:
        totalExpenses = data.text[data.text.find('$'):]

print(charityRegNo,"\n",charityWebsite,"\n",dateAsOf,"\n",description,"\n",re,"\n",totalRevenue,"\n",totalExpenses,"\n")
