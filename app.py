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
        timeout=7
    )
    gather.say(
        '<speak>Willkommen! <break time="300ms"/> Welcome! <break time="300ms"/> Добро пожаловать!</speak>',
        language="de-DE",
        voice="Polly.Vicki-Neural"
    )
    gather.say(
        '<speak>Für Deutsch drücken Sie eins.</speak>',
        language="de-DE",
        voice="Polly.Vicki-Neural"
    )
    gather.say(
        '<speak>For English, press two.</speak>',
        language="en-US",
        voice="Polly.Joanna-Neural"
    )
    gather.say(
        '<speak>Для русского языка нажмите три.</speak>',
        language="ru-RU",
        voice="Polly.Tatyana-Neural"
    )
    return Response(str(resp), mimetype='text/xml')

@app.route("/language_selected", methods=["POST"])
def language_selected():
    digit = request.form.get("Digits")
    resp = VoiceResponse()

    if digit == "1":
        lang = "de"
        resp.say(
            '<speak>Sie haben Deutsch gewählt. <break time="400ms"/> Wir beginnen jetzt das Gespräch.</speak>',
            language="de-DE",
            voice="Polly.Vicki-Neural"
        )
    elif digit == "2":
        lang = "en"
        resp.say(
            '<speak>You selected English. <break time="400ms"/> Let\'s start our conversation.</speak>',
            language="en-US",
            voice="Polly.Joanna-Neural"
        )
    elif digit == "3":
        lang = "ru"
        resp.say(
            '<speak>Вы выбрали русский язык. <break time="400ms"/> Начинаем разговор.</speak>',
            language="ru-RU",
            voice="Polly.Tatyana-Neural"
        )
    else:
        resp.say(
            '<speak>Неверный ввод. Попробуйте снова.</speak>',
            language="ru-RU",
            voice="Polly.Tatyana-Neural"
        )
        resp.redirect("/voice")
        return Response(str(resp), mimetype='text/xml')

    resp.redirect(f"/chat?lang={lang}")
    return Response(str(resp), mimetype='text/xml')

@app.route("/chat", methods=["POST", "GET"])
def chat():
    lang = request.args.get("lang", "de")
    resp = VoiceResponse()

    if lang == "de":
        resp.say("Das Gespräch beginnt auf Deutsch.", language="de-DE", voice="Polly.Vicki-Neural")
    elif lang == "en":
        resp.say("The conversation will be in English.", language="en-US", voice="Polly.Joanna-Neural")
    elif lang == "ru":
        resp.say("Разговор будет на русском языке.", language="ru-RU", voice="Polly.Tatyana-Neural")
    else:
        resp.say("Язык не распознан. Начинаем по умолчанию.", language="en-US", voice="Polly.Joanna-Neural")

    return Response(str(resp), mimetype='text/xml')