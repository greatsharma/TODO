import json
import re
import urllib
import requests

class BotConnector():
    
    def __init__(self, url):
        self.URL = url

    
    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode('utf8')

        return content

    
    def get_json_from_url(self, url):
        content = self.get_url(url)
        js_content = json.loads(content)

        return js_content


    def get_updates(self, offset=None):
        url = self.URL + 'getUpdates?timeout=100'

        if offset:
            url += '&offset={}'.format(offset)
            
        updates = self.get_json_from_url(url)

        return updates

    
    def send_message(self, chat_id, msg, reply_markup = None):
        msg = urllib.parse.quote_plus(msg)
        url = self.URL + 'sendMessage?chat_id={}&text={}'.format(chat_id, msg)
        
        if reply_markup:
            url += '&reply_markup={}'.format(reply_markup)
            
        self.get_url(url)


    def get_last_updateId(self, updates):
        num_updates = len(updates['result'])
        last_update_index = num_updates - 1
        
        last_update_id = updates['result'][last_update_index]['update_id']
        
        return last_update_id
