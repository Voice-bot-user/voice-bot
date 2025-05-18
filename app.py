from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/handle-language", method="POST")
    gather.say("Здравствуйте! Для продолжения выберите язык. Нажмите 1 для русского, 2 для немецкого, 3 для английского.", language="ru-RU")
    response.append(gather)
    response.redirect("/voice")  # если не выбрал — повтор
    return str(response)

@app.route("/handle-language", methods=["POST"])
def handle_language():
    digit = request.form.get("Digits")
    response = VoiceResponse()

    if digit == "1":
        response.say("Вы выбрали русский язык. Чем я могу помочь?", language="ru-RU")
    elif digit == "2":
        response.say("Sie haben Deutsch gewählt. Wie kann ich helfen?", language="de-DE")
    elif digit == "3":
        response.say("You have selected English. How can I help you?", language="en-US")
    else:
        response.say("Неверный выбор. Попробуйте снова.", language="ru-RU")
        response.redirect("/voice")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)