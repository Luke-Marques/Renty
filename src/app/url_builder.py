from abc import ABCMeta, abstractmethod
from enum import Enum


class SortType(Enum):
    def __str__(self):
        return str(self.value)

    OLDEST_LISTED = 10
    NEWEST_LISTED = 0
    HIGHEST_PRICED = 2
    LOWEST_PRICED = 1


class RegionIndex(Enum):
    def __str__(self):
        return str(self.value)

    BRISTOL = 219


class URLBuilder:
    base_url = "https://www.rightmove.co.uk/property-to-rent/find.html?"
    region_selected = False
    allowed_prices = [
        100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1100, 1200,
        1250, 1300, 1400, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3500, 3500, 4000, 4500,
        5000, 5500, 6000, 6500, 7000, 8000, 9000, 10000, 12500, 15000, 17500, 20000, 25000,
        30000, 35000, 40000
    ]
    allowed_furnish = ["furnished", "partFurnished", "unfurnished"]
    allowed_dont_show = ["houseShare", "retirement", "student"]
    allowed_must_have = ["student", "houseShare", "garden", "retirement", "parking"]
    allowed_properties = ["bungalow", "detached", "flat", "land", "park-home", "private-halls", "semi-detached",
                          "terraced"]

    def __init__(self):
        self.url = URLBuilder.base_url

    def sort_type(self, sort_type):
        self.url += "&sortType=" + str(sort_type)
        return self

    def min_bedrooms(self, no_bedrooms):
        self.url += "&minBedrooms=" + str(no_bedrooms)
        return self

    def max_bedrooms(self, no_bedrooms):
        self.url += "&maxBedrooms=" + str(no_bedrooms)
        return self

    def property_type(self, *argv):
        self.url += "&propertyTypes="
        for arg in argv:
            if arg not in self.allowed_properties:
                raise ValueError('Error! property type "' + str(arg) + '" not allowed')
            self.url += str(arg) + "%2C"
        return self

    def furnished_type(self, *argv):
        self.url += "&furnishType="
        for arg in argv:
            if arg not in self.allowed_furnish:
                raise ValueError('Error! Furnished type "' + str(arg) + '" not allowed')
            self.url += str(arg) + "%2C"
        return self

    def region(self, region_index):
        self.url += "&locationIdentifier=REGION%5E" + str(region_index)
        return self

    def must_have(self, *argv):
        self.url += "&mustHave="
        for arg in argv:
            if arg not in self.allowed_must_have:
                raise ValueError('Error! must have type "' + str(arg) + '" not allowed')
            self.url += str(arg) + "%2C"
        return self

    def dont_show(self, *argv):
        self.url += "&dontShow="
        for arg in argv:
            if arg not in self.allowed_dont_show:
                raise ValueError('Error! dont show "' + str(arg) + '" not allowed')
            self.url += str(arg) + "%2C"
        return self

    def min_price(self, price_per_month):
        if price_per_month not in self.allowed_prices:
            raise ValueError('Error! Price "' + str(price_per_month) + '" not allowed')
        self.url += "&minPrice=" + str(price_per_month)
        return self

    def max_price(self, price_per_month):
        if price_per_month not in self.allowed_prices:
            raise ValueError('Error! Furnished type "' + str(price_per_month) + '" not allowed')
        self.url += "&maxPrice=" + str(price_per_month)
        return self

    def show_let_agreed(self, show_let_agreed):
        self.url += "&includeLetAgreed=" + str(show_let_agreed)
        return self

    def set_page(self, page):
        self.url += "&index=" + str(page * 24)
        return self

    def get_result(self):
        return self.url


class URLSets:
    """The Director, building a complex representation."""

    @staticmethod
    def standard(page_no=0, num_beds=0):
        """Constructs and returns the final product"""
        return URLBuilder() \
            .region(RegionIndex.BRISTOL) \
            .set_page(page_no) \
            .sort_type(SortType.HIGHEST_PRICED) \
            .min_bedrooms(num_beds) \
            .max_bedrooms(num_beds) \
            .furnished_type("partFurnished", "unfurnished") \
            .get_result()

