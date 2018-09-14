import os
import sys
import json
import time
import random

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)
botName = 'Mocking SpongeBob'

@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  log('Recieved {}'.format(data))

  # We don't want to reply to ourselves!
  if data['name'] != botName:
    msg = random_uppercase(data['text'])
    send_message(msg)

  return "ok", 200

def random_uppercase(msg):
  msg = msg.join(random.choice([c.upper(), c ]) for c in msg )
  return msg

def send_message(msg):
  time.sleep(1) # prevent reply from showing before msg that bot is answering
  url  = 'https://api.groupme.com/v3/bots/post'
  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()
  
def log(msg):
  print(str(msg))
  sys.stdout.flush()
