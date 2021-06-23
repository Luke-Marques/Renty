import os
import time
import re
import requests
from bs4 import BeautifulSoup
import create_database as cdb
import data_to_tables as d2t


# identify self to robot.txt
headers = {
    'user-agent': 'Renty'
}


rightmove_bristol_base_url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E219' \
                             '&sortType=10''&index=??&propertyTypes=&includeSSTC=false&mustHave=&dontShow=' \
                             '&furnishTypes=&keywords= '


def get_searchResult_divs(base_url=None):
    """ searches for <div> tags with the class l-searchResult and returns all such tags
    :param base_url: the url for a rightmove webpage containing property listing cards
    :return: list of <div class='l-searchResult' ... > tags
    """

    # get html of base_url page
    if base_url is None:
        page = open(f'pages{os.sep}BristolPage.html', encoding='utf-8') # for testing
    else:
        r = requests.get(base_url, headers=headers)
        page = r.text

    # parse base_url page html text
    tree = BeautifulSoup(page, 'html.parser')
    better_file = tree.prettify()
    soup = BeautifulSoup(better_file, 'html.parser')

    # check if page has an error
    if soup.find_all(class_='l-container l-errorCard'):
        raise ValueError('Error! This page contains an error card.')

    # create empty list to store propertyCard tags
    propertyCard_divs = []

    # find all property_id divs in page
    divs = soup.findAll(class_='l-searchResult is-list')

    # remove property_id divs from divs if they are featured cards
    divs = [div for div in divs if not div.findAll(class_='propertyCard propertyCard--featured')]

    return divs


def get_data_from_searchResult_div(div):
    """ extracts data from various html tags contained within a <div> element
    :param div: html <div> element
    :return: tuples object containing data
    """

    # get property_id
    property_id = div['id']
    if 'property-' not in property_id:
        raise ValueError('Error! A "property-" was not found in property id tag.')
    else:
        property_id = property_id.replace('property-', '')

    # get title
    title_div = div.find('h2', class_='propertyCard-title')
    title = re.search('>(.*)</', str(title_div))

    # get price
    price_div = div.find(class_='propertyCard-priceValue')
    price = str(price_div)
    price = ''.join(price.splitlines())
    price = re.search('>(.*)</', price).group(1).strip()
    price = price.replace('£', '').replace(',', '')
    # price = float(price)

    # get location
    location_div = div.find(class_='propertyCard-address')
    location = str(location_div)
    location = ''.join(location.splitlines())
    location = re.search('<meta content=".*"/>(.*)</address>', location).group(1).strip()

    # get description
    description_div = div.find(class_='propertyCard-description')
    description = str(description_div)
    description = ''.join(description.splitlines())
    description = re.search('<span>(.*)</span></span>', description).group(1).strip()

    return (property_id, title, price, location, description)


# need to add mechanize function to get url of next page


def main():

    # creates db directory and file if they do not already exist
    # cdb.main()

    base_url = None

    database = f'{os.getcwd()}{os.sep}db{os.sep}listings.db'

    # loop through searchResult divs in url
    divs = get_searchResult_divs(base_url)
    count = 0
    for div in divs:
        # extract data from searchResult div
        data = get_data_from_searchResult_div(div)
        # connect to database
        # conn = d2t.create_connection(database)
        # update table
        # dt2.create_listing(conn, data)
        # commit changes to database
        # conn.commit()
        # conn.close()

        print(data)
        count += 1
    print(count)

if __name__ == '__main__':
    main()