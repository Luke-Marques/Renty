import math
import os
import time
import re
from enum import Enum
import requests
from bs4 import BeautifulSoup
import process_text
import create_database as cdb
import data_to_tables as d2t

from url_builder import URLSets

# identify self to robot.txt
headers = {'user-agent': 'Renty'}

PROPERTIES_PER_PAGE = 24

def get_soup(url=None):
    # get html of base_url page
    if url is None:
        page = open(f'pages{os.sep}BristolPage.html', encoding='utf-8')  # for testing
    else:
        r = requests.get(url, headers=headers)
        page = r.text

    if r.status_code != 200:
        raise ValueError('Error! A connection error')

    # parse base_url page html text
    tree = BeautifulSoup(page, 'html.parser')
    better_file = tree.prettify()
    soup = BeautifulSoup(better_file, 'html.parser')

    return soup


def get_property_cards(soup):
    """ searches for property card elements with the class l-searchResult within url html
    :param base_url: the url for a rightmove webpage containing property card elements
    :return: list of property card elements
    """

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

    # get number of bedrooms
    title_processed = process_text.lemmatize_string(title)
    if title_processed[1] == 'bedroom' and title_processed[0].isnumeric():
        num_bed = int(title_processed[0])
    elif 'studio' in title_processed:
        num_bed = 0
    else:
        num_bed = None

    # get type of property
    if num_bed == 0:
        property_type = 'studio'
    elif 'apartment' in title_processed:
        property_type = 'apartment'
    elif 'flat' in title_processed:
        property_type = 'flat'
    elif 'detach' in title_processed:
        property_type = 'detached house'
    elif 'terrace' in title_processed:
        property_type = 'terrace house'
    elif 'property' in title_processed:
        property_type = 'property'
    elif 'house' in title_processed:
        property_type = 'house'

    # get price
    price_element = property_card.find(class_='propertyCard-priceValue')
    price = str(price_element)
    price = ''.join(price.splitlines())
    price = re.search('>(.*)</', price).group(1).strip()
    price = price.replace('£', '').replace(',', '').replace(' pcm', '')
    price = int(price)
    # price = float(price)

    # get location
    location_element = property_card.find(class_='propertyCard-address')
    location = str(location_element)
    location = ''.join(location.splitlines())
    location = re.search('<span>(.*)</span>', location).group(1).strip()

    # get description
    description_element = property_card.find(class_='propertyCard-description')
    description = str(description_element)
    description = ''.join(description.splitlines())
    description = re.search('itemprop="description">(.*)</span>', description).group(1).strip()

    # get agent and agent_region
    agent_region_element = property_card.find('img', class_='propertyCard-branchLogo-image')
    agent_region = str(agent_region_element)
    agent_region = ''.join(agent_region.splitlines())
    if re.search('alt="(.*) Logo', agent_region) is not None:
        agent_region = re.search('alt="(.*) Logo', agent_region).group(1).strip()
        agent = agent_region.split(',')[0]
        agent_region = agent_region.split(',')[1]
    else:
        agent_region = None
        agent = None

    return property_id, title, num_bed, property_type, price, location, description, agent, agent_region

def get_number_of_pages(soup):
    result_count_element = soup.find(class_='searchHeader-resultCount')
    result_count = str(result_count_element)
    result_count = ''.join(result_count.splitlines())
    result_count = re.search('>(.*)</', result_count).group(1).strip()
    print(result_count)
    return math.ceil(int(result_count) / PROPERTIES_PER_PAGE)

def main():
    # creates db directory and file if they do not already exist
    # cdb.main()

    # url = None
    url = URLSets.standard(0)
    soup = get_soup(url)
    no_pages = get_number_of_pages(soup)
    property_cards = get_property_cards(soup)
    for page in range(0, no_pages):
        database = f'{os.getcwd()}{os.sep}db{os.sep}listings.db'
        # loop through searchResult divs in url
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
        time.sleep(1)
        url = URLSets.standard(page)
        soup = get_soup(url)
        property_cards = get_property_cards(soup)
    print("done")


if __name__ == '__main__':
    main()
