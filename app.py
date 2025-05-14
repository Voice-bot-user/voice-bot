from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    
    gather = Gather(
        input="dtmf", 
        timeout=5, 
        num_digits=1, 
        action="/language_selected", 
        method="POST"
    )
    
    gather.say(
        '<speak>'
        'Добро пожаловать! <break time="300ms"/> '
        'Для немецкого языка нажмите один. <break time="300ms"/> '
        'For English, press two. <break time="300ms"/> '
        'Для русского языка нажмите три.'
        '</speak>',
        language="ru-RU",
        voice="Polly.Tatyana-Neural"
    )
    
    resp.append(gather)
    resp.redirect("/voice")  # если нет ответа — повторяет

    return Response(str(resp), mimetype="text/xml")

@app.route("/language_selected", methods=["POST"])
def language_selected():
    digits = request.form.get('Digits')
    resp = VoiceResponse()

    if digits == "1":
        resp.say(
            '<speak>Вы выбрали немецкий язык. <break time="400ms"/> Начинаем разговор.</speak>',
            language="de-DE",
            voice="Polly.Vicki-Neural"
        )
    elif digits == "2":
        resp.say(
            '<speak>You selected English. <break time="400ms"/> Let\'s start the conversation.</speak>',
            language="en-US",
            voice="Polly.Joanna-Neural"
        )
    elif digits == "3":
        resp.say(
            '<speak>Вы выбрали русский язык. <break time="400ms"/> Начинаем разговор.</speak>',
            language="ru-RU",
            voice="Polly.Tatyana-Neural"
        )
    else:
        resp.say(
            '<speak>Неверный ввод. <break time="300ms"/> Попробуйте снова.</speak>',
            language="ru-RU",
            voice="Polly.Tatyana-Neural"
        )
        resp.redirect("/voice")
    
    return Response(str(resp), mimetype="text/xml")

if __name__ == "__main__":
    app.run()