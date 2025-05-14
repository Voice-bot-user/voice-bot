from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(_name_)

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    
    gather = Gather(input="dtmf", timeout=5, num_digits=1, action="/language_selected", method="POST")
    gather.say("Welcome! Press 1 for German. Press 2 for English. Press 3 for Russian.", language="en-US")
    
    resp.append(gather)
    resp.redirect("/voice")  # если человек ничего не нажал, повторить

    return Response(str(resp), mimetype="text/xml")

@app.route("/language_selected", methods=["POST"])
def language_selected():
    digits = request.form.get('Digits')
    resp = VoiceResponse()
    
    if digits == "1":
        resp.say("Sie haben Deutsch gewählt.", language="de-DE")
    elif digits == "2":
        resp.say("You selected English.", language="en-US")
    elif digits == "3":
        resp.say("Вы выбрали русский язык.", language="ru-RU")
    else:
        resp.say("Wrong input. Please try again.", language="en-US")
        resp.redirect("/voice")
    
    return Response(str(resp), mimetype="text/xml")

if _name_ == "_main_":
    app.run()