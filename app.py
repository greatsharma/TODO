import os
import todo_bot
from flask import Flask, request
from utils.db_helper import DBHelper
from utils.bot_connector import BotConnector


TOKEN = os.environ['TODO_TOKEN']
TODO_WEBHOOK_ENDPOINT = os.environ['TODO_WEBHOOK_ENDPOINT']    

conn = BotConnector(TOKEN)
# conn.set_webhook(TODO_WEBHOOK_ENDPOINT)


db = DBHelper('TODO_DB')
db.connect_db()
db.create_table('items', {'owner_id': 'text', 'list_name': 'text', 'item_name': 'text'})
db.create_index('items', 'owner_id', 'ownerIndex', 'ASC')
db.create_index('items', 'list_name', 'listIndex', 'ASC')
db.create_index('items', 'item_name', 'itemIndex', 'ASC')


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    todo_bot.update_dispatcher(conn, db, update)
    return ''


if __name__ == "__main__":
    app.run(debug=True)