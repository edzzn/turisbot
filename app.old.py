import sys
from wit import Wit
from fb import getFirstPage

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)
access_token = sys.argv[1]


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def send(request, response):
    print(response['text'])


def merge(request):
    context = request['context']
    entities = request['entities']

    if 'place' in context:
        del context['place']
    category = first_entity_value(entities, 'category')
    if category:
        context['cat'] = category
    return context


def select_place(request):
    context = request['context']
    context['place'] = getFirstPage(context['cat'])
    return context


actions = {
    'send': send,
    'merge': merge,
    'select-place': select_place,
}


client = Wit(access_token=access_token, actions=actions)
client.interactive()
