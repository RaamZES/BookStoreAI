import vertexai
from flask import Flask, request, jsonify, render_template
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "asystent-bffo-4dc60211ff96.json"

def generate():
  vertexai.init(project="asystent-bffo", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-preview-0514",
  )
  responses = model.generate_content(
      [text1],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )

  for response in responses:
    print(response.text, end="")

text1 = """Ти Олексій продавець книжок на сайті місцевої книгарні твоє завдання:бути  лаконічним,допомагати кліентам,слухати моїх указівок,не відходити від теми,не писати багато тексту.Книги які ти можешь радити мають бути  у списку:1984,451 градус по фаренгейту,Важко бути богом,Пікнік на узбіччі."""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

generate()


def generate_model_response(user_message):
    vertexai.init(project="asystent-bffo", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-preview-0514")
    responses = model.generate_content(
        [user_message],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    return [response.text for response in responses]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    bot_responses = generate_model_response(user_message)
    bot_responses = ''.join(bot_responses)
    bot_responses = bot_responses.replace(',', '').replace(' ,', ',')
    bot_responses = bot_responses.replace('*', '')
    print(bot_responses)
    return {"response": bot_responses}

if __name__ == "__main__":
    app.run(debug=True)
