# Implementes in Flask

from fb import getDataPage, searchPage
from wit import Wit

import json
import os
import logging
import logging.config
import ssl
import sys

import requests

from conversation import responder
from flask import Flask, request

# Declare some constants
FB_VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']
# FB_PAGE_ID = os.environ['FB_PAGE_ID']
FB_ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']
WIT_TOKEN = os.environ['WIT_TOKEN']

# Setup Flask  Server
app = Flask(__name__)
logger = logging.getLogger(__name__)

# Facebook Messenger GET Webhook
@app.route('/', methods=['GET'])
def verify_webhook():
    # When the endpoint is registered as a webhook, it must
    # return the 'hub.challenge' value in the query arguments.
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == correct_token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Ready to talk!", 200


if __name__ == '__main__':
    # Run Server
    app.run(host='0.0.0.0', port=argv[1])
