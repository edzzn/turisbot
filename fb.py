import requests
import os

token = FB_ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']

# set info


def setSearchIdsUrl(topic):
    latitude = "-2.9183953"
    longitude = "-79.0362543"
    radio = "5000"  # en metros
    return ("https://graph.facebook.com/v2.8/search?q=" + topic +
            "&type=place&center=" + latitude + "%2C" + longitude + "&distance="
            + radio + "&access_token=" + token)


# def setSearchPageUrl(topic):
#     latitude = "-2.9183953"
#     longitude = "-79.0362543"
#     radio = "5000"  # en metros
#     return ("https://graph.facebook.com/v2.8/" + topic +
#             "?fields=about%2Clocation%2Coverall_star_rating%2Cratings%7B" +
#             "rating%2Chas_rating%7D%2Cpicture%7Burl%7D%2Cname%2C" +
#             "hours&access_token=" + token)


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
    print(requests['data'][0]['name'])
    return(requests['data'][0]['name'])


def getDataPage(query):
    requests = getDataUrl(setSearchIdsUrl(query))
    # print(requests)
    if 'data' in requests and len(requests['data']) > 0:
        return(requests['data'])
    elif 'error' in requests:
        print(requests['error']['message'])
        return None
    else:
        print('No data')
        return None


# list the ids of Pages


def listIdPages(data):
    for place in data['data']:
        print(place['id'])

# writes in a .txt file the id of the pages


def writeIdPages(data, fileId):
    for place in data['data']:
        fileId.write(place['id'] + ": " + place['name'] + '\n')
        print(place['id'] + ": " + place['name'])

# listIdPages(getDataUrl(setSearchIdsUrl('pizza')))

# writeIdPages(getDataUrl(setSearchIdsUrl('pizza')))


# getFirstPage("italian")
