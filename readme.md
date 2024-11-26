# Healthcare Translation Web App

A simple web application that enables real-time multilingual translation for healthcare providers and patients. The app includes voice-to-text transcription, text translation, and audio playback for the translated text.

---

## Features
- **Voice-to-Text**: Convert spoken words into text using browser speech recognition.
- **Text Translation**: Translate text into multiple languages (e.g., Spanish, French, German) using LibreTranslate API.
- **Text-to-Speech**: Play the translated text as audio using Google Text-to-Speech (gTTS).
- **Rate Limiting**: Prevent excessive API calls with Flask-Limiter.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Pip

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Healthcare-Translation-App.git
   cd Healthcare-Translation-App
