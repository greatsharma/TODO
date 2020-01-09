from flask import Flask, request


TOKEN = os.environ['TODO_TOKEN']
TODO_WEBHOOK_ENDPOINT = os.environ['TODO_WEBHOOK_ENDPOINT']

conn = BotConnector(TOKEN)
#conn.set_webhook(TODO_WEBHOOK_ENDPOINT)
