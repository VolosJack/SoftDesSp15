"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def build_url(place_name):
    """
    Take an address encode for a query.

    :param str param_dict: parameters with associated values
    >>> build_url("Fenway Park")
    'https://maps.googleapis.com/maps/api/geocode/json?address=Fenway+Park'
    """
    p = {"address" : place_name}

    full_url = GMAPS_BASE_URL +"?" +urllib.urlencode(p)

    return full_url

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    >>> get_json("https://maps.googleapis.com/maps/api/geocode/json?address=Fenway%20Park")
    {u'status': u'OK', u'results': [{u'geometry': {u'location_type': u'APPROXIMATE', u'bounds': {u'northeast': {u'lat': 42.3472515, u'lng': -71.0943879}, u'southwest': {u'lat': 42.345397, u'lng': -71.0989444}}, u'viewport': {u'northeast': {u'lat': 42.3476732302915, u'lng': -71.0943879}, u'southwest': {u'lat': 42.3449752697085, u'lng': -71.0989444}}, u'location': {u'lat': 42.3466764, u'lng': -71.0972178}}, u'address_components': [{u'long_name': u'Fenway Park', u'types': [u'establishment'], u'short_name': u'Fenway Park'}, {u'long_name': u'4', u'types': [u'street_number'], u'short_name': u'4'}, {u'long_name': u'Yawkey Way', u'types': [u'route'], u'short_name': u'Yawkey Way'}, {u'long_name': u'West Fens', u'types': [u'neighborhood', u'political'], u'short_name': u'West Fens'}, {u'long_name': u'Boston', u'types': [u'locality', u'political'], u'short_name': u'Boston'}, {u'long_name': u'Suffolk County', u'types': [u'administrative_area_level_2', u'political'], u'short_name': u'Suffolk County'}, {u'long_name': u'Massachusetts', u'types': [u'administrative_area_level_1', u'political'], u'short_name': u'MA'}, {u'long_name': u'United States', u'types': [u'country', u'political'], u'short_name': u'US'}, {u'long_name': u'02215', u'types': [u'postal_code'], u'short_name': u'02215'}], u'place_id': u'ChIJbz8lP_Z544kRBFV6ZMsNgKI', u'formatted_address': u'Fenway Park, 4 Yawkey Way, Boston, MA 02215, USA', u'types': [u'stadium', u'establishment']}]}
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    return json.loads(response_text)

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    :param str place_name: name or address
    >>> get_lat_long("Fenway Park")
    (42.3466764, -71.0972178)
    """
    url = build_url(place_name)

    response_json = get_json(url)
    lat_lng = [response_json["results"][0]["geometry"]["location"]["lat"], response_json["results"][0]["geometry"]["location"]["lng"]]
    return lat_lng[0], lat_lng[1]

def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    >>> get_nearest_station(42.3466764, -71.0972178)
    ('Brookline Ave opp Yawkey Way', 0.0881209298968315)
    """
    lat = {"lat": latitude}
    lng = {"lon": longitude}
    api_key = {"api_key": MBTA_DEMO_API_KEY}
    url = MBTA_BASE_URL + "?" + urllib.urlencode(api_key)+"&"+ urllib.urlencode(lat)+"&"+urllib.urlencode(lng)+"&format=json"
    response_json = get_json(url)
    name_dis = (str(response_json["stop"][0]["stop_name"]), float(response_json["stop"][0]["distance"]))
    return name_dis

def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the 
    distance from the given place to that stop.
    >>> find_stop_near("Fenway Park")
    ('Brookline Ave opp Yawkey Way', 0.0881209298968315)
    """
    lat_lng = get_lat_long(place_name)
    # print lat_lng[0]
    stop = get_nearest_station(lat_lng[0], lat_lng[1])
    return stop


if __name__ == "__main__":
    import doctest

    doctest.testmod()
