from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
from sense_hat import SenseHat

sense = SenseHat()

app = Flask(__name__)
ask = Ask(app, "/alexa_pi")

def update_sense_hat():
    pass

@app.route('/')
def homepage():
    return "welcome to AlexaPi!"
    
@ask.launch
def start_skill():
    welcome_message = "Hello there! How can I help you today?"
    return question(welcome_message)

@ask.intent("SwitchonIntent")
def switchon_intent():
    #do some sense control
    #sense.show_message("power on")
    sense.show_letter('o')
    msg = 'Ok! Message displayed!'
    return statement(msg)

@ask.intent("SwitchoffIntent")
def switchoff_intent():
    #sense.show_message("power off")
    sense.clear()
    msg = 'Powered off and message displayed'
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)