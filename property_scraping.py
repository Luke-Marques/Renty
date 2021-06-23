import os
import time
import re
import requests
from bs4 import BeautifulSoup
import create_database as cdb
import data_to_tables as d2t

# identify self to robot.txt
headers = {'user-agent': 'Renty'}

rightmove_bristol_base_url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E219' \
                             '&sortType=10''&index=??&propertyTypes=&includeSSTC=false&mustHave=&dontShow=' \
                             '&furnishTypes=&keywords= '


def get_property_cards(base_url=None):
    """ searches for property card elements with the class l-searchResult within url html
    :param base_url: the url for a rightmove webpage containing property card elements
    :return: list of property card elements
    """

    # get html of base_url page
    if base_url is None:
        page = open(f'pages{os.sep}BristolPage.html', encoding='utf-8')  # for testing
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

    # find all property card elements in page
    property_cards = soup.findAll(class_='l-searchResult is-list')

    # remove property card elements from list if they are featured cards
    property_cards = [pc for pc in property_cards if not pc.findAll(class_='propertyCard propertyCard--featured')]

    return property_cards


def get_data_from_property_card(property_card):
    """ scrapes data from various html tags contained within a property card element
    :param property_card: html element with class='l-searchResult'
    :return: scraped data
    """

    # get property_id
    property_id = property_card['id']
    if 'property-' not in property_id:
        raise ValueError('Error! A "property-" was not found in property id tag.')
    else:
        property_id = property_id.replace('property-', '')

    # get title
    title_element = property_card.find('h2', class_='propertyCard-title')
    title = str(title_element)
    title = ''.join(title.splitlines())
    title = re.search('>(.*)</', title).group(1).strip()

    # get price
    price_element = property_card.find(class_='propertyCard-priceValue')
    price = str(price_element)
    price = ''.join(price.splitlines())
    price = re.search('>(.*)</', price).group(1).strip()
    price = price.replace('£', '').replace(',', '')
    # price = float(price)

    # get location
    location_element = property_card.find(class_='propertyCard-address')
    location = str(location_element)
    location = ''.join(location.splitlines())
    location = re.search('<meta content=".*"/>(.*)</address>', location).group(1).strip()

    # get description
    description_element = property_card.find(class_='propertyCard-description')
    description = str(description_element)
    description = ''.join(description.splitlines())
    description = re.search('<span>(.*)</span></span>', description).group(1).strip()

    return property_id, title, price, location, description


def main():

    # creates db directory and file if they do not already exist
    # cdb.main()

    base_url = None

    database = f'{os.getcwd()}{os.sep}db{os.sep}listings.db'

    # loop through searchResult divs in url
    property_cards = get_property_cards(base_url)
    count = 0
    for property_card in property_cards:
        # extract data from property card element
        data = get_data_from_property_card(property_card)
        # connect to database
        # conn = d2t.create_connection(database)
        # update database table
        # dt2.create_listing(conn, data)
        # commit changes to database
        # conn.commit()
        # conn.close()

        print(data)
        count += 1
    print(count)


if __name__ == '__main__':
    main()
