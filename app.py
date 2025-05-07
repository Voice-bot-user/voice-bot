from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    gather = resp.gather(
        num_digits=1,
        action="/language_selected",
        method="POST",
        timeout=5
    )
    gather.say("Willkommen! Welcome! Добро пожаловать!", language="de-DE")
    gather.say("Für Deutsch drücken Sie eins.", language="de-DE")
    gather.say("For English, press two.", language="en-US")
    gather.say("Для русского языка нажмите три.", language="ru-RU")
    return Response(str(resp), mimetype='text/xml')

@app.route("/language_selected", methods=["POST"])
def language_selected():
    digit = request.form.get("Digits")
    resp = VoiceResponse()

    if digit == "1":
        lang = "de"
        resp.say("Вы выбрали немецкий.", language="de-DE")
    elif digit == "2":
        lang = "en"
        resp.say("You selected English.", language="en-US")
    elif digit == "3":
        lang = "ru"
        resp.say("Вы выбрали русский язык.", language="ru-RU")
    else:
        resp.say("Неверный ввод. Попробуйте снова.", language="ru-RU")
        resp.redirect("/voice")
        return Response(str(resp), mimetype='text/xml')

    resp.redirect(f"/chat?lang={lang}")
    return Response(str(resp), mimetype='text/xml')

@app.route("/chat", methods=["POST", "GET"])
def chat():
    lang = request.args.get("lang", "de")
    resp = VoiceResponse()

    if lang == "de":
        resp.say("Das Gespräch beginnt auf Deutsch.", language="de-DE")
    elif lang == "en":
        resp.say("The conversation will be in English.", language="en-US")
    elif lang == "ru":
        resp.say("Разговор будет на русском языке.", language="ru-RU")
    else:
        resp.say("Язык не распознан. Начинаем по-умолчанию.", language="en-US")

    return Response(str(resp), mimetype='text/xml')