from flask import Flask
from threading import Thread
import os
import time

global stop_threads

app = Flask('')

@app.route('/')
def home():
  return "Bot is online"

@app.route('/bastet-goddess.jpg')
def bgjpg():
  # this works
  # return "Duh!"

  # this does not work
  return send_file('bastet-goddess.jpg', mimetype='image/jpeg')

def run(stop):
  while True:
    app.run(host='0.0.0.0',port=8080)
    time.sleep(1)
    if stop():
      break

def keep_alive(stop_threads):
  t = Thread(target=run, args =(lambda : stop_threads, ))
  t.start()

  
