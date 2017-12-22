# =========================================================
# Author:
#     Rodolfo Ferro Pérez
#     ferro(at)cimat(dot)mx
#
# Alexa skill to gather Python news from Reddit
# =========================================================

from flask_ask import Ask, statement, question, session
from credentials import *
from pprint import pprint
from flask import Flask
import unidecode
import requests
import logging
import json
import time

# Set global variables
name = 'Rodolfo'

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


# Create Flask, Ask apps
app = Flask(__name__)  # Standard Flask app
ask = Ask(app, "/reddit_python")  # App endpoint


# App route
@app.route("/")
def homepage():
    return "Hey there {}! Flask is running with no problems!".format(name)


# Alexa initial message (starting app...)
@ask.launch
def start_skill():
    welcome_msg = "Hi {}, would you like to hear any Python toppics on Reddit?".format(name)
    return question(welcome_msg)


# If answer is yes
@ask.intent("YesIntent")
def share_headlines():
    python_headlines = reddit_python_headlines()
    headline_msg = "The current Python headlines on Reddit are: {}.".format(python_headlines)
    return statement(headline_msg)


# If answer is no
@ask.intent("NoIntent")
def no_intent():
    bye_text = "Okay, good bye."
    return statement(bye_text)


# End session
@ask.session_ended
def session_ended():
    log.debug("Session ended.")
    return "", 200


# Consume Reddit API
def reddit_python_headlines():
    # # Login url and metadata
    # reddit_url = "https://www.reddit.com/api/login"
    # user_pass_dict = {'user': REDDIT_USER,
    #                   'passwd': REDDIT_PASSWORD,
    #                   'api_type': 'json'}
    #
    # # Create a session
    # sess = requests.Session()
    # sess.headers.update({'User-Agent': 'Python Reddit headlines with Alexa'})
    # sess.post(reddit_url, data=user_pass_dict)
    # time.sleep(1)   # Wait for connection...

    # Consume Reddit's API to gather info
    url = "https://www.reddit.com/r/Python/.json?limit=10"
    # html = sess.get(url)
    html = requests.get(url)
    info = json.loads(html.content.decode('utf-8'))
    pprint(info)
    child = info['data']['children']
    titles = [unidecode.unidecode(elem['data']['title']) for elem in child]
    titles = "... ".join([title for title in titles])

    return titles


if __name__ == "__main__":
    app.run(debug=True)
