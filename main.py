import requests
from bs4 import BeautifulSoup
import re
r = requests.get('https://www.rightmove.co.uk/property-for-sale/find.html?includeSSTC=false&keywords=&sortType=2'
                 '&viewType=LIST&channel=BUY&index=0&maxPrice=210000&radius=0.5&locationIdentifier=POSTCODE%5E103844'
                 '#prop108774380')
# print(r.text)

soup = BeautifulSoup(r.text, 'html.parser')
listofproperties = soup.findAll('div', class_='l-searchResult is-list')

formatted_links = []

for card in listofproperties:
    pricetag = card.find_all('div', class_='propertyCard-priceValue')
    price = re.findall(r"(?:[\£\$\€]{1}[,\d]+.?\d*)", (str(pricetag)))
    data = {
        'price': price,
    }
    formatted_links.append(data)

print(formatted_links)
