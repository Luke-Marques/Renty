import math
import os
import time
import re
import requests
from bs4 import BeautifulSoup
from sqlite3 import Error
from tqdm import tqdm

import process_text
from database_builder import DatabaseBuilder

from url_builder import URLSets


# identify self to robot.txt
headers = {'user-agent': 'Renty'}

PROPERTIES_PER_PAGE = 24


def get_soup(url=None):
    # get html of base_url page
    if url is None:
        page = open(f'pages{os.sep}BristolRents.html', encoding='utf-8')  # for testing
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
    :param soup:
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
    if len(title_processed) > 1:
        if title_processed[1] == 'bedroom' and title_processed[0].isnumeric():
            num_bed = int(title_processed[0])
        elif 'studio' in title_processed:
            num_bed = 0
        else:
            num_bed = -1

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
            property_type = 'terraced house'
        elif 'property' in title_processed:
            property_type = 'property'
        elif 'house' in title_processed:
            property_type = 'house'
        elif 'park' in title_processed:
            property_type = 'parking'
        elif 'private' in title_processed and 'hall' in title_processed:
            property_type = 'private halls'
        else:
            print(title_processed)
            property_type = None
    else:
        num_bed = -1
        property_type = None

    # get price
    price_element = property_card.find(class_='propertyCard-priceValue')
    price = str(price_element)
    price = ''.join(price.splitlines())
    price = re.search('>(.*)</', price).group(1).strip()
    price = price.replace('£', '').replace(',', '').replace(' pcm', '')
    try:
        price = int(price)
    except ValueError:
        price = -1
    # price = float(price)

    # get address and postcode
    address_element = property_card.find(class_='propertyCard-address')
    address = str(address_element)
    address = ''.join(address.splitlines())
    address = re.search('<span>(.*)</span>', address).group(1).strip()
    try:
        postcode = re.search(r'[A-Za-z]{1,2}\d{1,2}', address.upper()).group(0).strip()
    except AttributeError:
        postcode = None

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

    return property_id, title, num_bed, property_type, price, description, agent, agent_region, address, postcode


def get_number_of_pages(soup):
    result_count_element = soup.find(class_='searchHeader-resultCount')
    result_count = str(result_count_element)
    result_count = ''.join(result_count.splitlines())
    result_count = re.search('>(.*)</', result_count).group(1).strip()
    num_pages = math.ceil(int(result_count) / PROPERTIES_PER_PAGE)
    print('Number of pages :', num_pages)
    return num_pages


def main():
    basepath = os.path.dirname(__file__)
    dbpath = os.path.abspath(os.path.join(basepath,os.pardir, "renty.db"))
    print(dbpath)
    db = DatabaseBuilder(dbpath)
    db.new_table('properties')
    db.new_table('dates')

    # loop through possible number of beds
    print('GETTING RENTAL PROPERTY DATA')
    print('----------------------------')
    for num_beds in range(11):
        print('Number of beds  :', num_beds)
        url = URLSets.standard(num_beds=num_beds)
        soup = get_soup(url)
        num_pages = get_number_of_pages(soup)
        for page in range(num_pages):
            print('Page            :', page, end='')
            url = URLSets.standard(page_no=page, num_beds=num_beds)
            soup = get_soup(url)
            property_cards = get_property_cards(soup)
            print()
            for property_card in (property_cards):
                data = get_data_from_property_card(property_card)
                try:
                    db.insert_data('properties', data)
                except Error as e:
                    print(e)
        print('----------------------------')
    time.sleep(1)


if __name__ == '__main__':
    main()
