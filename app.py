from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    resp.say("Привет! Ваш звонок успешно принят. Оставайтесь на линии.", language="ru-RU")
    return Response(str(resp), mimetype='text/xml')

if __name__ == "__main__":
    app.run()