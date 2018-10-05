import os
import sys
import json
import time
import random

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)
botName = os.getenv('BOT_NAME')

@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  log('Received {}'.format(data))
  percent = float(os.getenv('REPLY_CHANCE'))
  targeted_userid = os.getenv('TARGETED_USERID') # if 0, targets everyone

  if (data['name'] != botName):
    if random.random() <= percent:
      if data['sender_id'] == targeted_userid or (targeted_userid == '0'):
        if data['text'] != '':
          log('Sending reply')
          msg = random_uppercase(data['text'])
          send_message(msg)
        else:
          log('Not sending reply - blank message')
      else:
        log('Not sending reply - not the targeted user')
    else:
      log('Not sending reply - chance')


  return "ok", 200

def random_uppercase(msg):
  msg = ''.join(random.choice([c.upper(), c.lower()]) for c in msg)
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
