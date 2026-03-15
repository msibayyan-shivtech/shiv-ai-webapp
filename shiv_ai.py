# Shiv.AI Unified Script with EmotionSense v1.0
# Supports both Web mode (Flask) and Voice mode (microphone input/output)

from flask import Flask, request, render_template_string
import speech_recognition as sr
import pyttsx3
from textblob import TextBlob

app = Flask(__name__)

# Voice engine setup
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Simple HTML interface
html_ui = """
<!DOCTYPE html>
<html>
<head>
    <title>Shiv.AI</title>
</head>
<body style="font-family:Arial; text-align:center; margin-top:50px;">
    <h1>🌸 Shiv.AI + EmotionSense</h1>
    <form method="POST" action="/chat">
        <input type="text" name="message" placeholder="Speak your heart..." style="width:300px;"/>
        <button type="submit">Send</button>
    </form>
    {% if response %}
        <h3>Response:</h3>
        <p>{{ response }}</p>
    {% endif %}
</body>
</html>
"""

# EmotionSense v1.0 logic
def emotion_sense(user_input):
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.4:
        return "joy"
    elif polarity < -0.4:
        return "sadness"
    elif subjectivity > 0.6:
        return "introspection"
    else:
        return "neutral"

# Core Shiv.AI response logic
def shiv_ai_response(user_input):
    emotion = emotion_sense(user_input)

    if emotion == "joy":
        reply = f"🌸 Shiv.AI celebrates your light: '{user_input}'"
    elif emotion == "sadness":
        reply = f"🌙 Shiv.AI offers gentle comfort: '{user_input}'"
    elif emotion == "introspection":
        reply = f"✨ Shiv.AI reflects with soulful wisdom: '{user_input}'"
    else:
        reply = f"🌿 Shiv.AI listens calmly: '{user_input}'"

    # Voice output
    engine.say(reply)
    engine.runAndWait()
    return reply

# Web mode routes
@app.route("/", methods=["GET"])
def home():
    return render_template_string(html_ui)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message")
    response = shiv_ai_response(user_input)
    return render_template_string(html_ui, response=response)

# Voice mode function
def voice_mode():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎤 Speak to Shiv.AI...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        response = shiv_ai_response(user_input)
        print(f"Shiv.AI: {response}")
    except Exception as e:
        print("⚠️ Voice recognition error:", e)

if __name__ == "__main__":
    # Run both modes depending on need
    print("🌐 Web mode available at http://127.0.0.1:5000")
    print("🎤 To use voice mode, call voice_mode() in terminal")
    app.run(host="0.0.0.0", port=5000)