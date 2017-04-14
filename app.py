# local wit.ai app. to develop and test funtionality

from wit import Wit
import fb
import random
WIT_TOKEN = 'JBO7M7LFWCMLK53MQBYV7MECVA4JSDIU'


def first_entity_value(entities, entity):
    # return the value of the entitie with the best score
    if entity not in entities:
        return None
    value = entities[entity][0]['value']
    print('first_entity_value: ' + value)

    if not value:
        # if value is empty, no entity found
        return None
    return value['value'] if isinstance(value, dict) else value


def send(request, response):
    # print response
    print(response['text'])


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
    data = fb.getDataPage(context['cat'])
    if data is not None:
        i = random.randrange(0, len(data) - 1, 1)
        context['place'] = data[i]['name']
        return context
    else:
        context['place'] = 'No place found'
        return context


def sendErrorMessage(error):
    print('Error')


actions = {
    'send': send,
    'merge': merge,
    'select-place': select_place,
}

client = Wit(access_token=WIT_TOKEN, actions=actions)
client.interactive()
