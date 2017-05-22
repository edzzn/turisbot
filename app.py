import os
from wit import Wit
import requests
from bottle import Bottle, request, debug, response
from fb import getDataPage, searchPage
from random import randrange
from sys import argv

# Declare some constants
FB_VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']
FB_PAGE_ID = os.environ['FB_PAGE_ID']
FB_ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']
WIT_TOKEN = os.environ['WIT_TOKEN']



# Setup Bottle Server
debug(True)
app = Bottle()


# Facebook Messenger GET Webhook
@app.get('/webhook')
def messenger_webhook():
    verify_token = request.query.get('hub.verify_token')
    if verify_token == FB_VERIFY_TOKEN:
        challenge = response.status = 200
        challenge = request.query.get('hub.challenge')
        return challenge
    else:
        return 'Invalid Request or Verification Token'

# Facebook Messenger POST Webhook
@app.post('/webhook')
def messenger_post():
    """ Maneja el webhook"""
    data = request.json
    print('Data Received:')
    print(data)

    # asegura que es una subcripcion de una pagina
    if data['object'] == 'page':

        for entry in data['entry']:
            messages = entry['messaging']

            if messages[0]:
                message = messages[0]
                fb_id = message['sender']['id']
                text = message['message']['text']

                # fb_generic_message(fb_id)
                # fb_message(fb_id, 'Texto No generico')
                # fb_boton_message(fb_id,"Texto sobre el boton")
                client.run_actions(session_id=fb_id, message=text)


    else:
        # Returned another event
        return 'Received Different Event'
    return None


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


def fb_generic_message(sender_id, pages_id, maxi = 5):

    elements = []
    if len(pages_id) < maxi:
        maxi = len(pages_id) - 1

    element = {
                "title":"Welcome to Peter\'s Hats",
                "image_url":"https://edzzn.com/",
                "subtitle":"We\'ve got the right hat for everyone.",
                "default_action": {
                  "type": "web_url",
                  "url": "https://edzzn.com/",

                  "webview_height_ratio": "tall",
               #    "fallback_url": "https://edzzn.com/"
                },
                "buttons":[
                  {
                    "type":"web_url",
                    "url":"https://petersfancybrownhats.com",
                    "title":"View Website"
                  },{
                    "type":"postback",
                    "title":"Start Chatting",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD"
                  }
                ]
              }


    for i in range(maxi):
        page_info = searchPage(pages_id[i])
        elem_i = {
                    "title":page_info['name'],
                    "image_url": page_info['picture']['data']['url'],
                    "subtitle":page_info['about'],
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


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def send(request, response):
    # sender function
    fb_id = request['session_id']
    text = response['text']
    print('Fb_di: %s, Text: %s' %(fb_id, response))
    fb_message(fb_id, text)


def merge(request):
    # get the context, type
    context = request['context']
    entities = request['entities']
    print('In merge(), context: ' + str(context) +
          ' entities:' + str(entities))

    if 'place' in context:
        del context['place']
    category = first_entity_value(entities, 'category')
    if category:
        context['cat'] = category
    if 'ack' in context:
        print(context['ack'])
        del context['ack']
    return context


def select_place(request):
    context = request['context']
    data = getDataPage(context['cat'])
    if data is not None:

        fb_id = request['session_id']
        fb_generic_message(fb_id, data, 5)


        # try:
        #     i = randrange(0, len(data))
        # except:
        #     i = 0
        # dataPage = searchPage(data[i]['id'])
        # msj = data[i]['name']
        # if 'street' in dataPage['location']:
        #     msj = msj + ", esta en las calles: " + str(dataPage['location']['street'])
        # if 'overall_star_rating' in dataPage:
        #     msj = msj + " y tiene un promedio de " + \
        #         str(dataPage['overall_star_rating']) + ' estrellas'
        # context['place'] = msj
        return context
    else:
        fb_id = request['session_id']
        fb_message(fb_id, "No se encontro el lugar, intenta con otro")
        # context['place'] = 'No se encontro el lugar, intenta con otro'
        return context


# Setup Actions
actions = {
    'send': send,
    'merge': merge,
    'select-place': select_place,
}

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN, actions=actions)

if __name__ == '__main__':
    # Run Server
    app.run(host='0.0.0.0', port=argv[1])
