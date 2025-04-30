from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import openai

openai.api_key = "вставь_сюда_свой_OpenAI_API_ключ"

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get('SpeechResult', 'Привет! Чем могу помочь?')

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    ai_reply = response['choices'][0]['message']['content']

    twiml = VoiceResponse()
    twiml.say(ai_reply, voice='alice', language='en-US')

    return str(twiml)

if __name__ == "__main__":
    app.run(debug=True, port=5000)