from flask import Flask, request, jsonify, render_template
from gtts import gTTS
import os
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Rate Limiter Configuration
limiter = Limiter(get_remote_address, app=app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    spoken_text = request.json.get('spoken_text', '')
    if not spoken_text:
        return jsonify({"error": "No spoken text provided"}), 400
    return jsonify({"transcript": spoken_text})

@app.route('/translate', methods=['POST'])
@limiter.limit("10 per minute")
def translate():
    data = request.json
    print(f"Received data: {data}")  # Log incoming request data

    original_text = data.get('text')
    target_language = data.get('language', 'es')  # Default to Spanish

    if not original_text:
        return jsonify({"error": "No text provided for translation"}), 400

    # Log the translation request data
    print(f"Text to translate: {original_text}, Target language: {target_language}")

    try:
        # Use MyMemory API for free translation
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": original_text, "langpair": f"en|{target_language}"}
        )
        translation_data = response.json()
        translation = translation_data.get("responseData", {}).get("translatedText", "")

        if not translation:
            return jsonify({"error": "Translation failed, please try again"}), 500

        print(f"Translated text: {translation}")  # Log the translated text
        return jsonify({"translation": translation})

    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text', '')
    language = request.json.get('language', 'es')  # Default to Spanish

    if not text:
        return jsonify({"error": "No text provided for speech"}), 400

    try:
        audio_path = "static/output.mp3"
        tts = gTTS(text=text, lang=language)
        tts.save(audio_path)
        return jsonify({"audio_url": f"/{audio_path}"}), 200
    except Exception as e:
        print(f"Error during speech synthesis: {e}")  # Log error for debugging
        return jsonify({"error": f"Speech synthesis failed: {str(e)}"}), 500

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error. Please try again later."}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found."}), 404

if __name__ == '__main__':
    if not os.path.exists("static"):
        os.makedirs("static")  # Ensure the 'static' directory exists
    app.run(debug=True)
