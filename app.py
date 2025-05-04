from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    resp.say("Привет! Это голосовой бот на Render и Twilio.", language="ru-RU")
    return str(resp)
