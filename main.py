import csv
import time

import requests
from bs4 import BeautifulSoup
import re

headers = {
    'user-agent': 'Renty',
}

duplicate_count = 0
max_duplicate_count = 3

propertyData = []

class urlManager:
    index = 0
    base_url = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E219&sortType=10" \
               "&index=??&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords= "

    def UpdatedUrl(self):
        return self.base_url.replace("index=??", "index=" + str(self.index))


def ParseTagForPropertyID(tag):
    global duplicate_count, propertyData, max_duplicate_count
    property_id = tag['id']
    if "property-" not in property_id:
        return 0
    if tag.find_all(class_="propertyCard propertyCard--featured"):
        return 0
    property_id = property_id.replace("property-", "")
    for property_values in propertyData:
        if property_id == property_values:
            duplicate_count += 1
            print("Duplicate")
            if duplicate_count == max_duplicate_count:
                print("Too many Duplicate")
                return -1
            return 0
    duplicate_count = 0
    return property_id


def GetPropertiesFromPage(url):
    # r = requests.get(url, headers=headers)
    # page_html = r.text
    page_html = open("pages\\BristolPage.html", encoding='utf-8')

    tree = BeautifulSoup(page_html, "html.parser")
    better_file = tree.prettify()
    soup = BeautifulSoup(better_file, "html.parser")

    if soup.find_all(class_="l-container l-errorCard"):
        print("End of the road")
        return True

    for tag in soup.select('div[id]'):
        property_id = ParseTagForPropertyID(tag)
        if property_id == -1:
            return 1
        if property_id == 0:
            continue
        propertyData.append(property_id)

    file = open('data.txt', 'w')
    for items in propertyData:
        file.writelines(items+"\n")
    file.close()
    return 0


def main():
    bristol = urlManager()
    upto_date = False
    while not upto_date:
        print("Page: " + str(bristol.index/24))
        upto_date = GetPropertiesFromPage(bristol.UpdatedUrl())
        bristol.index = bristol.index + 24
        time.sleep(1)


if __name__ == '__main__':
    main()

