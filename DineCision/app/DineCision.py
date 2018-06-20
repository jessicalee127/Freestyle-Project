import argparse
import json
import pprint
import requests
import sys
import urllib
import random


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode



# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= "9aFYynAfext2uPCBlmYUdjsE_yKyue5f010epOxkBJ-qQnxSu1hTAmFZlLk2oJEorEbQopfTe5y4r08p70YaXd7zRpeUw9E6dKEEb7uMSN_U1i_921-UAqsj48UhW3Yx"




# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'New York City, NY'
SEARCH_LIMIT = 5


def yelprequest(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return yelprequest(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return yelprequest(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)


def main():
    #   TODO: CHANGE TO USER INPUT
    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
    #                     type=str, help='Search term (default: %(default)s)')
    # parser.add_argument('-l', '--location', dest='location',
    #                     default=DEFAULT_LOCATION, type=str,
    #                     help='Search location (default: %(default)s)')


    #input_values = parser.parse_args()
    location_input = input("Please enter the area you want to search for (e.g. 3 Times Square, New York City): ")
    rating_input = input("Do you care about ratings (e.g. 4 or 4.5): ")
    price_input = input("Do you care about price (e.g. 1 is the lowest, 4 is the highest): ")

    url_params = {
        'location': location_input.replace(' ', '+'),
        'radius': 500,
        'is_closed': "false",
        'rating': rating_input,
        'limit': SEARCH_LIMIT,
        'categories': "restaurants, All",
        'price': price_input
    }

    recommendation = []
    result = yelprequest(API_HOST, SEARCH_PATH, API_KEY, url_params)
    business_list = result["businesses"]
    random_business = random.choice(business_list)
    print("Please go to " + random_business["name"] + " !")
    Show_more = input("Do you want to learn more about it: ")
    if Show_more == "yes":
        print(random_business)
    else:
        print("enjoy!")

    # try:
    #     query_api(input_values.term, input_values.location)
    # except HTTPError as error:
    #     sys.exit(
    #         'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
    #             error.code,
    #             error.url,
    #             error.read(),
    #         )
    #     )


if __name__ == '__main__':
    main()
