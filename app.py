
from flask import Flask, request, Response
import openai
import os

app = Flask(_name_)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/voice", methods=["POST"])
def voice():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты — голосовой ассистент."},
            {"role": "user", "content": "Скажи что-нибудь приветственное"}
        ]
    )
    text = response.choices[0].message.content

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{text}</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)