# Renty 

## Setup 

1. To use a virtual environment `virtualenv venv -p python3` in the project directory
2. Active it `source venv/bin/activate`

## Goal
Provide historic data about the propery market 

- Bedrooms : Card/Search
- Property Type (House, Flat, etc) : Card
- Approx Address : Card
- Letting Agent : Card
- Listing Data : Local and Card
- Let Data : Local and Card
- Removal : Local

- Shared : Card/Search
- Student : Search
- Retirement Property : Search

- Price : Card


## Creating URLS

### property_type()

For property type, you can enter as many options as the following options:
`"bungalow", "detached", "flat", "land", "park-home", "private-halls", "semi-detached", "terraced"`
If not used, all property types are shown. 

### sort_type()

There are four sort types, you can acess them though the class `SortType`. They are
`OLDEST_LISTED, NEWEST_LISTED, HIGHEST_PRICED, LOWEST_PRICED`
If not used, it will default to NEWEST_LISTED.

### furnished_type()

For funished type, you can enter as many options as the following options:
`"furnished", "partFurnished", "unfurnished".`
If not used, all furnished types are shown.

### min_bedrooms() and max_bedrooms()

For bedrooms, enter any number between 0 and 10. 0 is for a studio.
If not used, min_bedrooms() is taken as 0, and max_bedrooms has no limit. 

### dont_show()

For dont show, you can enter as many options as the following options to not show:
`"houseShare", "retirement", "student"`
If not used, all the above will be shown.

### must_have()

For must have, you can enter as many options as the following options:
`"student", "houseShare", "garden", "retirement", "parking"`
If not used, properties with and outwith these will be shown. 

### region()

Only supports the RegionIndex type, which currently has option(s):
BRISTOL
If this is not used, it will default to BRISTOL.

### min_price() and max_price()

For min price and max price you can enter any of the following values (in PCM):
100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1250, 1300, 1400, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3500, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 8000, 9000, 10000, 12500, 15000, 17500, 20000, 25000, 30000, 35000, 40000
If not used, all price ranges will be available. 

### show_let_agreed()

Enter one of the below options: 
`"false", "true"`
If not used, it will be set to false.