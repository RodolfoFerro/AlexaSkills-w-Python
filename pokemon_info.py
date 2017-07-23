# =========================================================
# Author:
#     Rodolfo Ferro Pérez
#     ferro(at)cimat(dot)mx
#
# Alexa skill to gather Pokemon info from PokeAPI
# =========================================================

from flask import Flask
from flask_ask import Ask, statement, question, session
import requests, json, unidecode, time, logging

# Set global variables
name = 'Rodolfo'

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Create Flask, Ask apps
app = Flask(__name__) # Standard Flask app
ask = Ask(app, "/poke_info") # App endpoint

# App route
@app.route("/")
def homepage():
    return "Hey there {}! Flask is running with no problems!".format(name)

# Alexa initial message (starting app...)
@ask.launch
def start_skill():
    welcome_msg = "Hello there {}, would you like me to give you any Pokemon's info?".format(name)
    return question(welcome_msg)

# If answer is yes
@ask.intent("YesIntent")
def yes_intent():
    poke_msg = "What Pokemon's info would you like? Tell me an ID number please."
    return question(poke_msg)

# Ask for Pokémon
@ask.intent("PokeIntent", convert={'pokemonid': int})
def poke_intent(pokemonid):
    poke_msg = get_poke_info(pokemonid)
    return statement(poke_msg)

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

# Get poke info
def get_poke_info(pokemonid):
    # Set url and do request
    url = "http://pokeapi.co/api/v2/pokemon/"
    response  = requests.get(url + str(pokemonid))
    poke_data = ""

    # Construct answer
    if response.ok:
        data = response.json()
        poke_data += "The Pokemon is " + data['name'][0].upper() + data['name'][1:] + "... "
        poke_data += "It's height is " + str(data['height']/10) + " meters... "
        poke_data += "And it's weight is " + str(data['weight']/10) + " kilograms... "
    else:
        poke_data += "Sorry, I wasn't able to find info about a Pokemon with that ID."

    return poke_data
    

if __name__ == "__main__":
    app.run(debug=True)
