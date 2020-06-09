#!/usr/bin/env python
# coding: utf-8

# ## Functions
# ---
#
# This file contains script for extracting metadata from imagery and external details from Google and Zillow APIs.
#
# External data from the following APIs are extracted:
# - Google Street View API
# - Google Geocoder API
# - Zillow individual house prices and details
#
# **Note: In order to use these APIs, keys from Google and Zillow must be obtained.**

# In[1]:


# Modules that need to be installed are pillow, google_streetview, googlemaps, pygeocoder
py_modules =['pillow','google_streetview', 'googlemaps','pygeocoder']

## Install the following modules in your device
# %pip install pillow
# %pip install google_streetview
# %pip install googlemaps
# %pip install pygeocoder
# %pip install pyzillow


# In[3]:


## Pillow is used to extract data from Imagery ##


# Importing the image library pillow

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Import google_streetview for the api module
import googlemaps
import google_streetview.api
import google_streetview

import json

# Importing for reversing to the address

from pygeocoder import Geocoder

def get_exif(filename):
    """Function for extracting GPS data from image
        Args:
            img (.jpeg / .png et al.): an image file Note: Photos
        Output:
            Will first validate whether or not we have a valid image file and then output the
            metadata in form of a dictionary """
    try:
        image = Image.open(filename)
        image.verify()    #Image verify won't output anything if the image is in the correct format
        exif = image._getexif()
        if exif is not None:
            for key, value in exif.items():
                name = TAGS.get(key, key)
                exif[name] = exif.pop(key)

    except:
        raise ValueError("""Please upload a valid jpg or png file do not use airdrop or messaging apps like WhatsApp
                         or Slack to transfer images. Emailing will keep all of the metadata.""")


    return exif



def get_geotagging(exif):


    """ Returns:
        Dictionary with following key: value pairs:
            'GPSVersionID':  bytes,
            'GPSLatitudeRef': str = 'N' or 'S',
            'GPSLatitude': tuple of tuples,
            'GPSLongitudeRef': str = 'E' or 'W',
            'GPSLongitude': tuple of tuples,
            'GPSAltitudeRef': byte string,
            'GPSAltitude': tuple,
            'GPSTimeStamp': tuple of tuples,
            'GPSSatellites':,
            'GPSStatus':,
            'GPSMeasureMode':,
            'GPSDOP':,
            'GPSSpeedRef': str,
            'GPSSpeed': tuple,
            'GPSImgDirectionRef': str,
            'GPSImgDirection': tuple,
            'GPSDestBearingRef': str,
            'GPSDestBearing': tuple,
            'GPSDateStamp': str representing datetime,
            'GPSDifferential',
            'GPSHPositioningError': tuple,
            'GPSTrackRef',
            'GPSTrack',
            'GPSMapDatum',
            'GPSDestLatitudeRef',
            'GPSDestLatitude',
            'GPSDestLongitudeRef',
            'GPSDestLongitude',
            'GPSDestDistanceRef',
            'GPSDestDistance',
            'GPSProcessingMethod',
            'GPSAreaInformation',

                }
    """

    if not exif:
        raise ValueError("No metadata found please check your camera settings")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            geotagging= exif[tag]

    new = {GPSTAGS[k]: v for k,v in geotagging.items()}

    return new

# # Convert to degrees


def to_degrees(coord,direc):
    deg_num, deg_denom = coord[0]
    d = float(deg_num)/float(deg_denom)

    min_num, min_denom = coord[1]
    m = float(min_num)/float(min_denom)
    #Seconds are optional
    try:
        sec_num, sec_denom = coord[2]
        s = float(sec_num)/float(sec_denom)
    except:
        s = 0

    if direc == 'N' or direc == 'E':
        sign = 1
    elif direc == 'S' or direc == 'W':
        sign = -1


    return sign*(d + m/(60.00)+s/(3600.00))


# ## Putting in the Google API

view = google_streetview

with open('credentials.json') as json_file:
    credential = json.load(json_file)



gmaps = googlemaps.Client(credential['google-api-key'])

# Define parameters for street view api
def google_streetviewer(location, key='YOURAPIKEY'):
    params = [{
    'size': '600x300', # max 640x640 pixels
    'location': location ,
    'heading': '151.78',
    'pitch': '-0.76',
    'key': key
    }]

    # Create a results object
    results = google_streetview.api.results(params)

    # Download images to directory 'downloads'
    return results.download_links('google-pics')



# ## Setting up the Google API to show the address


def reverse_lookup(lat, long, key='YOURAPIKEY'):
    """Function for lookup of addresses from latitude, longitude details using Google Maps API
    Args:
        lat (float): latitude as float
        long (float): longitude as float
        key (str): (default='YOURAPIKEYHERE') google maps api key
    Returns:
        returns a tuple with address (str), zipcode (str)
        """
    result = str(Geocoder(api_key=key).reverse_geocode(lat, long))
    location_details = result.split(",")
    address = location_details[0]
    zipcode = location_details[-2]
    city = location_details[1]
    state = location_details[2].split(" ")[1]
    return address, zipcode, city, state

## Setting up the Zillow API

#Packages used for the Zillow API

from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails

def zillow_query(key, address,citystatezip):

    zillow =[]
    zillow_data =  ZillowWrapper(key)
    deep_search_response = zillow_data.get_deep_search_results(
        address, citystatezip)
    result = GetDeepSearchResults(deep_search_response)


#Print the results of the query

    return result


foo = zillow_query(credential['zillow-api-key'], '108 S Croft', '90048')



a = foo.__dict__


a


# ## Function that gets the metadata and gives all the details about the location


def master_query(img_file):
    exif = get_exif(img_file)
    tags = get_geotagging(exif)
    location = f"{to_degrees(tags['GPSLongitude'], tags['GPSLongitudeRef'])},{to_degrees(tags['GPSLatitude'], tags['GPSLatitudeRef'])}"

    google_view = google_streetviewer(location, key= credential['google-api-key'])

    address = reverse_lookup(float(location.split(",")[1]),float(location.split(",")[0]), credential['google-api-key'])

    details = zillow_query(credential['zillow-api-key'],address[0],address[1])
    details_dict = details.__dict__
    keys = ['zillow_id','home_type','year_built','property_size','home_size',
            'bathrooms','bedrooms','last_sold_date','last_sold_price','zestimate_amount']
    dict_outcome= {k:a[k] for k in keys if k in a}
    return dict_outcome
