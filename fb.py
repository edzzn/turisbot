import requests
import os
from pprint import pprint as pp

try:
    FB_ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']
except:
    FB_ACCESS_TOKEN = ""


def setToken():
    global FB_ACCESS_TOKEN
    FB_ACCESS_TOKEN = raw_input('Token: >')



# set info


def setSearchIdsUrl(topic):
    latitude = "-2.9183953"
    longitude = "-79.0362543"
    radio = "5000"  # en metros
    return ("https://graph.facebook.com/v2.8/search?q=" + topic +
            "&type=place&center=" + latitude + "%2C" + longitude + "&distance="
            + radio + "&access_token=" + FB_ACCESS_TOKEN)

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
    # pp(requests['data'][0]['name'])
    return(requests['data'][0]['name'])


def getDataPage(query):
    requests = getDataUrl(setSearchIdsUrl(query))
    # print(requests)
    if 'data' in requests:
        # check if data is empty
        if requests['data']:
            # print('FB.py sent data - getDataPage()')
            # pp(requests['data'])
            return(requests['data'])

    elif 'error' in requests and len(requests['data']) > 0:
        print(requests['error']['message'])
        return None
    else:
        print('No data')
        return None


def searchPage(pageId):
    url = ("https://graph.facebook.com/v2.8/" + pageId + "?fields=name%2Cabout%2Coverall_star_rating%2Clocation%2Cpicture&access_token=" + FB_ACCESS_TOKEN)
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


def fb_message(sender_id, text):
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # prepare query
    qs = 'access_token=' + FB_ACCESS_TOKEN
    # send post request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content


def fb_boton_message(sender_id, text_boton):
    data = {
    "recipient":{"id" : sender_id},
     "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text":text_boton,
            "buttons":[
              {
                "type":"web_url",
                "url":"https://edzzn.com",
                "title":"Show Website"
              },
              {
                "type":"postback",
                "title":"Start Chatting",
                "payload":"USER_DEFINED_PAYLOAD"
              }
              ]
          }
        }
      }
    }
    # prepare query
    qs = 'access_token=' + FB_ACCESS_TOKEN
    # send post request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content


def fb_generic_message(sender_id, pages_id, maxi):

    elements = []
    if len(pages_id) < maxi:
        maxi = len(pages_id) - 1

    # element = {
    #             "title":"Welcome to Peter\'s Hats",
    #             "image_url":"https://edzzn.com/",
    #             "subtitle":"We\'ve got the right hat for everyone.",
    #             "default_action": {
    #               "type": "web_url",
    #               "url": "https://edzzn.com/",
    #
    #               "webview_height_ratio": "tall",
    #            #    "fallback_url": "https://edzzn.com/"
    #             },
    #             "buttons":[
    #               {
    #                 "type":"web_url",
    #                 "url":"https://petersfancybrownhats.com",
    #                 "title":"View Website"
    #               },{
    #                 "type":"postback",
    #                 "title":"Start Chatting",
    #                 "payload":"DEVELOPER_DEFINED_PAYLOAD"
    #               }
    #             ]
    #           }


    for i in range(maxi):
        page_info = searchPage(pages_id[i]['id'])
        try:
            about =  page_info['about']
        except:
            about = "Tiene un promedio de: " + str(page_info['overall_star_rating']) + " estrellas"

        elem_i = {
                    "title":page_info['name'],
                    "image_url": page_info['picture']['data']['url'],
                    "subtitle":about,
                    "default_action": {
                      "type": "web_url",
                      "url": "https://www.facebook.com/" + page_info['id'],

                    #   "webview_height_ratio": "tall",
                   #    "fallback_url": "https://edzzn.com/"
                    },
                    "buttons":[
                      {
                        "type":"web_url",
                        "url":"https://www.messenger.com/t/" +page_info['id'],
                        "title":"Enviar un mensaje"
                      }
                    #   ,{
                    #     "type":"postback",
                    #     "title":"Start Chatting",
                    #     "payload":"DEVELOPER_DEFINED_PAYLOAD"
                    #   }
                    ]
                  }
        elements.append(elem_i)



    data = {
    "recipient":{"id" : sender_id},
     "message":{
         "attachment":{
           "type":"template",
           "payload":{
             "template_type":"generic",
             "elements": elements
           }
         }
      }
    }


    # prepare query
    qs = 'access_token=' + FB_ACCESS_TOKEN
    # send post request to messenger
    resp = requests.post('https://graph.facebook.com/v2.6/me/messages?' + qs,
                         json=data)
    return resp.content
