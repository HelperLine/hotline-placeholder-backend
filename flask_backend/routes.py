
from flask import request
from flask_backend import app
from twilio.twiml.voice_response import VoiceResponse, Gather

from flask_backend.hotline_translation import hotline_translation


@app.route("/")
def index():
    return "<p>\"Helperline\" Hotline. See our <a href='https://helperline.io/'>Website</a> for more.</p>"


@app.route("/hotline", methods=['GET', 'POST'])
def initial_endpoint():

    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.redirect(f'/hotline/de/initial')
            return str(resp)
        elif choice == '2':
            resp.redirect(f'/hotline/en-gb/initial')
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say(hotline_translation["choose_language_unknown"]["de"], voice="woman", language="de")
            resp.say(hotline_translation["choose_language_unknown"]["en-gb"], voice="woman", language="en-gb")

    # Start our <Gather> verb
    gather = Gather(num_digits=1)
    gather.say(hotline_translation["choose_language"]["de"], voice="woman", language="de")
    gather.say(hotline_translation["choose_language"]["en-gb"], voice="woman", language="en-gb")
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect(f'/hotline')

    return str(resp)


@app.route("/hotline/<language>/initial", methods=['GET', 'POST'])
def endpoint_with_language(language):
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say(hotline_translation["shut_down_message"][language], voice="woman", language=language)
    resp.say(hotline_translation["goodbye_message"][language], voice="woman", language=language)

    return str(resp)
