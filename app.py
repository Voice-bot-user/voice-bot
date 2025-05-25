import os
from flask import Flask, request, url_for
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)
LANG = "ru-RU"

@app.route("/voice", methods=["POST"])
def voice():
    print("===> voice() called")
    resp = VoiceResponse()
    resp.say("Здравствуйте! Нажмите 1 для русского языка.", language=LANG)
    resp.redirect(url_for("handle_language", _external=True))
    return str(resp)

@app.route("/handle_language", methods=["POST"])
def handle_language():
    digit = request.form.get("Digits")
    print("===> handle_language() called, Digit =", digit)
    resp = VoiceResponse()

    # Пропускаем выбор языка, сразу переходим к следующему
    resp.say("Переходим к выбору направления.", language=LANG)
    resp.redirect(url_for("handle_topic", _external=True))
    return str(resp)

@app.route("/handle_topic", methods=["POST"])
def handle_topic():
    digit = request.form.get("Digits")
    print("===> handle_topic() called, Digit =", digit)
    resp = VoiceResponse()

    resp.say("Вы дошли до раздела выбора направления. Всё работает.", language=LANG)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)