from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/handle-language", method="POST")
    gather.say("Здравствуйте! Для продолжения выберите язык. Нажмите 1 для русского, 2 для немецкого, 3 для английского.", language="ru-RU")
    response.append(gather)
    response.redirect("/voice")  # если пользователь ничего не нажал
    return str(response)

@app.route("/handle-language", methods=["POST"])
def handle_language():
    digit = request.form.get("Digits")
    response = VoiceResponse()

    if digit == "1":
        gather = Gather(num_digits=1, action="/handle-topic", method="POST")
        gather.say("Спасибо, продолжаем на русском. Выберите направление: 1 — солнечные панели, 2 — тепловые насосы, 3 — другие вопросы.", language="ru-RU")
        response.append(gather)
        return str(responce)

    elif digit == "2":
        response.say("Deutsch folgt demnächst.", language="de-DE")
    elif digit == "3":
        response.say("English support is coming soon.", language="en-US")
    else:
        response.say("Неверный выбор. Попробуйте снова.", language="ru-RU")
        response.redirect("/voice")

    return str(response)

@app.route("/handle-topic", methods=["POST"])
def handle_topic():
    digit = request.form.get("Digits")
    response = VoiceResponse()

    if digit == "1":
        response.say("Вы выбрали солнечные панели. Хотите: 1 — передать информацию в технический отдел, 2 — получить консультацию.", language="ru-RU")
        # сюда можно вставить новый Gather с action="/handle-solar"
    elif digit == "2":
        response.say("Вы выбрали тепловые насосы. Хотите: 1 — передать информацию в технический отдел, 2 — получить консультацию.", language="ru-RU")
        # сюда можно вставить новый Gather с action="/handle-heat"
    elif digit == "3":
        response.say("Опишите ваш вопрос, и мы вам поможем.", language="ru-RU")
        # можно добавить запись или перевод на человека
    else:
        response.say("Неверный выбор. Попробуйте снова.", language="ru-RU")
        response.redirect("/voice")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)