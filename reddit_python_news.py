# =========================================================
# Author:
#     Rodolfo Ferro Pérez
#     ferro(at)cimat(dot)mx
#
# Alexa skill to gather Python news from Reddit
# =========================================================

from flask import Flask
from flask_ask import Ask, statement, question, session
import requests, json, unidecode, time, logging

# Set global variables
name = 'INSERT_YOUR_NAME_HERE'

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Create Flask, Ask apps
app = Flask(__name__) # Standard Flask app
ask = Ask(app, "/reddit_python") # App endpoint

# App route
@app.route("/")
def homepage():
    return "Hey there {}! Flask is running with no problems!".format(name)

# Alexa initial message (starting app...)
@ask.launch
def start_skill():
    welcome_msg = "Hello there {}, would you like to hear any Python toppics on Reddit?".format(name)
    return question(welcome_message)

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
    # Login url and metadata
    reddit_url = "https://www.reddit.com/api/login"
    user_pass_dict = {'user': 'INSERT_REDDIT_USER_HERE',
                      'passwd': 'INSERT_REDDIT_PASS_HERE',
                      'api_type': 'json'}

    # Create a session
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'Python Reddit headlines with Alexa'})
    sess.post(reddit_url, data=user_pass_dict)
    time.sleep(1)   # Wait for connection...

    # Consume Reddit's API to gather info
    url  = "https://www.reddit.com/r/Python/.json?limit=10"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [ unidecode.unidecode(listing['data']['title']) for listing in data['data']['children'] ]
    titles = "... ".join([title for title in titles])

    return titles

if __name__ == "__main__":
    app.run(debug=True)
