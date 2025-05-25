import os
from flask import Flask, request, url_for
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)
LANG = "ru-RU"

@app.route("/voice", methods=["POST"])
def voice():
    print("===> voice() called")
    resp = VoiceResponse()
    resp.say("Здравствуйте! Начинаем демонстрацию маршрута.", language=LANG)
    resp.redirect(url_for("handle_language", _external=True))
    return str(resp)

@app.route("/handle_language", methods=["POST"])
def handle_language():
    print("===> handle_language() called")
    resp = VoiceResponse()
    resp.say("Переходим к выбору темы.", language=LANG)
    resp.redirect(url_for("handle_topic", _external=True))
    return str(resp)

@app.route("/handle_topic", methods=["POST"])
def handle_topic():
    print("===> handle_topic() called")
    resp = VoiceResponse()
    resp.say("Вы выбрали солнечные панели.", language=LANG)
    resp.redirect(url_for("handle_solar", _external=True))
    return str(resp)

@app.route("/handle_solar", methods=["POST"])
def handle_solar():
    print("===> handle_solar() called")
    resp = VoiceResponse()
    resp.say("Информация передана в технический отдел. Спасибо.", language=LANG)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)