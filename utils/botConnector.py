import json
import re
import urllib
import requests

class BotConnector():
    # make timeout a property
    
    def __init__(self, token):
        self.base_url_ = f'https://api.telegram.org/bot{token}/'

    def _get_url(self, url):
        response = requests.get(url)
        response = response.content.decode('utf8')
        return json.loads(response)

    def set_webhook(self, endpoint):
        print('\nsetting webhook...(this may take a while)')
        url = self.base_url_ + f'setWebhook?url={endpoint}'
        response = self._get_url(url)
        if not response['ok']:
            raise Exception('unable to set webhook!')

    def get_updates(self, offset=None):
        url = self.base_url_ + 'getUpdates?timeout=100'
        if offset:
            url += '&offset={}'.format(offset)
        updates = self._get_url(url)
        return updates

    
    def send_message(self, chat_id, msg, reply_markup = None):
        msg = urllib.parse.quote_plus(msg)
        url = self.base_url_ + 'sendMessage?chat_id={}&text={}'.format(chat_id, msg)
        if reply_markup:
            url += '&reply_markup={}'.format(reply_markup)  
        self._get_url(url)


    def get_last_updateId(self, updates):
        num_updates = len(updates['result'])
        last_update_index = num_updates - 1
        last_update_id = updates['result'][last_update_index]['update_id']
        return last_update_id
