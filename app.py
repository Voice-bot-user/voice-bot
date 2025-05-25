
   import os
from flask import Flask, request, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)
LANG = "ru-RU"


@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    g = Gather(
        num_digits=1,
        action=url_for("handle_language", _external=True),
        method="POST",
        timeout=5,
    )
    g.say(
        "Здравствуйте! Для продолжения выберите язык. Нажмите 1 для русского.",
        language=LANG,
    )
    resp.append(g)
    return str(resp)


@app.route("/handle_language", methods=["POST"])
def handle_language():
    digit = request.form.get("Digits")
    resp = VoiceResponse()

    if digit == "1":
        g = Gather(
            num_digits=1,
            action=url_for("handle_topic", _external=True),
            method="POST",
            timeout=5,
        )
        g.say(
            "Спасибо, продолжаем на русском. "
            "Выберите направление: 1 — солнечные панели, 2 — тепловые насосы, 3 — другие вопросы.",
            language=LANG,
        )
        resp.append(g)
    else:
        resp.say("Выбранный язык пока не поддерживается. Попробуйте снова.", language=LANG)
        resp.redirect(url_for("voice", _external=True))

    return str(resp)


@app.route("/handle_topic", methods=["POST"])
def handle_topic():
    digit = request.form.get("Digits")
    resp = VoiceResponse()

    if digit == "1":
        g = Gather(
            num_digits=1,
            action=url_for("handle_solar", _external=True),
            method="POST",
            timeout=5,
        )
        g.say(
            "Вы выбрали солнечные панели. "
            "Нажмите 1 — передать информацию в технический отдел, "
            "2 — получить консультацию.",
            language=LANG,
        )
        resp.append(g)

    elif digit == "2":
        g = Gather(
            num_digits=1,
            action=url_for("handle_heat", _external=True),
            method="POST",
            timeout=5,
        )
        g.say(
            "Вы выбрали тепловые насосы. "
            "Нажмите 1 — передать информацию в технический отдел, "
            "2 — получить консультацию.",
            language=LANG,
        )
        resp.append(g)

    elif digit == "3":
        resp.say("Опишите ваш вопрос, и мы поможем. Спасибо!", language=LANG)
    else:
        resp.say("Неверный выбор. Попробуйте снова.", language=LANG)
        resp.redirect(url_for("handle_language", _external=True))

    return str(resp)


def _final(theme: str, digit: str) -> VoiceResponse:
    resp = VoiceResponse()

    if digit == "1":
        resp.say(
            "Спасибо. Ваша информация передана в технический отдел. "
            "Мы свяжемся с вами в ближайшее время.",
            language=LANG,
        )
    elif digit == "2":
        resp.say(
            f"Я — консультант и могу рассказать о {theme}. "
            "Задайте ваш вопрос.",
            language=LANG,
        )
    else:
        resp.say("Неверный выбор. Возвращаюсь в главное меню.", language=LANG)
        resp.redirect(url_for("voice", _external=True))

    return resp


@app.route("/handle_solar", methods=["POST"])
def handle_solar():
    return str(_final("солнечных системах", request.form.get("Digits")))


@app.route("/handle_heat", methods=["POST"])
def handle_heat():
    return str(_final("тепловых насосах", request.form.get("Digits")))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)