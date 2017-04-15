import os
import requests
# FB_ACCESS_TOKEN = os.environ["FB_ACCESS_TOKEN"]
FB_ACCESS_TOKEN = 'EAAECnMYc2p0BAOep93FbOAu3p2FuTx14YghZA6CE2PIZCjwfbuZAbGDwMqLWY2Dz5KgagKSbyZCql6w0ZChZCaf5TR7mux5bms01TojRLL3MWJw3IBuc3BbNcFPClLNRVkqJKfGn9Wg8UBWMxJoPnox7D5d9ssIrOfTBa6iZBoylXYBZCIOmVGXZAUFeqVuwXsmIZD'

token = FB_ACCESS_TOKEN

# set info


def setSearchIdsUrl(topico):
    topic = topico
    latitude = "-2.9183953"
    longitude = "-79.0362543"
    radio = "5000"  # en metros
    return ("https://graph.facebook.com/v2.8/search?q=" + topic + "&type=place&center=" + latitude + "%2C" + longitude + "&distance=" + radio + "&access_token=" + token)


def setSearchPageUrl(id):
    topic = topico
    latitude = "-2.9183953"
    longitude = "-79.0362543"
    radio = "5000"  # en metros
    return "https://graph.facebook.com/v2.8/" + id + "?fields=about%2Clocation%2Coverall_star_rating%2Cratings%7Brating%2Chas_rating%7D%2Cpicture%7Burl%7D%2Cname%2Chours&access_token=" + token


# funtion that from a Url outputs jsonData
def getDataUrl(url):
    webURL = requests.get(url)

    # webURL = request.query_string(url)
    # data = webURL.read()
    # encoding = webURL.info().get_content_charset('utf-8')
    return webURL.json()


def getFirstPage(query):
    data = getDataUrl(setSearchIdsUrl(query))
    return(data['data'][0]['name'])


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


# combine the url getting
# reads the list.txt file, search graph.api for every item in it
# then saves every ID found with the item search in a listIds.txt file
# fileList = open('list.txt', 'r')
# data = fileList.read().replace('\n', ',').replace(' ', '')
# # data[:-1] deletes the last item in the vector
# dataVector = data[:-1].split(',')
# fileId = open('listIds.txt', 'w')
# for topic in dataVector:
#     # print (topic)
#
#     url = setSearchIdsUrl(topic)
#     dataUrl = getDataUrl(url)
#     # listIdPages(dataUrl)
#     writeIdPages(dataUrl, fileId)
#
# fileList.close()
# fileId.close()


# get data from topic
# getFirstPage('italiano')
