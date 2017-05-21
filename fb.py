import requests
import os
from pprint import pprint as pp

token = FB_ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']

def setToken():
    global token
    token = raw_input('Token: >')



# set info


def setSearchIdsUrl(topic):
    latitude = "-2.9183953"
    longitude = "-79.0362543"
    radio = "5000"  # en metros
    return ("https://graph.facebook.com/v2.8/search?q=" + topic +
            "&type=place&center=" + latitude + "%2C" + longitude + "&distance="
            + radio + "&access_token=" + token)

# funtion that from a Url outputs jsonData


def getDataUrl(url):
    webURL = requests.get(url)
    return webURL.json()


def getFirstPage(query):
    requests = getDataUrl(setSearchIdsUrl(query))
    print(requests)
    if 'error' in requests:
        print(requests['error']['message'])
        return None
    if 'data' not in requests:
        print('No data')
        return None
    print("Facebook Data: \n Query: %s" %query)
    pp(requests['data'][0]['name'])

    return(requests['data'][0]['name'])


def getDataPage(query):
    requests = getDataUrl(setSearchIdsUrl(query))
    # print(requests)
    if 'data' in requests:
        # check if data is empty
        if requests['data']:
            print('FB.py sent data - getDataPage()')
            pp(requests['data'])
            return(requests['data'])

    elif 'error' in requests and len(requests['data']) > 0:
        print(requests['error']['message'])
        return None
    else:
        print('No data')
        return None


def searchPage(pageId):
    url = ("https://graph.facebook.com/v2.8/" + pageId + "?fields=name%2C" +
           "location%2Coverall_star_rating&access_token=" + token)
    requests = getDataUrl(url)
    print(requests)
    if 'name' in requests:
        print('FB.py sent data')
        print("Facebook Data: \n PageId: %s" % pageId)
        pp(requests)
        return(requests)
    elif 'error' in requests:
        print(requests['error']['message'])
        return None
    else:
        print('No data')
        return None


def listIdPages(data):
    # list the ids of Pages
    for place in data['data']:
        print(place['id'])

# writes in a .txt file the id of the pages


def writeIdPages(data, fileId):
    for place in data['data']:
        fileId.write(place['id'] + ": " + place['name'] + '\n')
        print(place['id'] + ": " + place['name'])
