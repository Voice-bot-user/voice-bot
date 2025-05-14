from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    resp.say("Hello! Your call was received successfully!", language="en-US")
    return Response(str(resp), mimetype="text/xml")

if __name__ == "__main__":
    app.run()