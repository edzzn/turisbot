import os
from wit import Wit
import requests
from bottle import Bottle, request, debug, response
from fb import getDataPage, searchPage, fb_generic_message, fb_message
from random import randrange
from sys import argv

# Declare some constants
FB_VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']
# FB_PAGE_ID = os.environ['FB_PAGE_ID']
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
        response.status = 200
        challenge = request.query.get('hub.challenge')
        return challenge
    else:
        return 'Invalid Request or Verification Token'


# Facebook Messenger POST Webhook
@app.post('/webhook')
def messenger_post():
    data = request.json
    print('Data Received')
    print(data)
    if data['object'] == 'page':
        for entry in data['entry']:
            messages = entry['messaging']
            if messages[0]:
                # Get the first message
                message = messages[0]
                fb_id = message['sender']['id']
                text = message['message']['text']
                if text == "Hola" or text == "hola":
                    fb_message(fb_id, 'Hola, Puedes preguntar por cualquier lugar de tu interes. :)')
                else:
                    client.run_actions(session_id=fb_id, message=text)
    else:
        # Returned another event
        return 'Received Different Event'
    return None


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
    print('Fb_di:')
    print(fb_id)
    print('text: ')
    print(response)
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
        fb_generic_message(sender_id=fb_id,pages_id=data,maxi=4)
        context['place'] = ''
        return context
    else:
        context['place'] = 'No se encontraron lugares :/'
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
