// Handle Transcribe Button
document.getElementById("transcribeButton").onclick = async () => {
    const audioData = "sample audio data"; // Replace with actual audio data
    try {
        const response = await fetch("/transcribe", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ audio: audioData }),
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById("originalTranscript").innerText = data.transcript;
        } else {
            alert("Error in transcription: " + data.error);
        }
    } catch (error) {
        console.error("Transcription failed:", error);
    }
};

// Handle Translate Button
document.getElementById("translateButton").onclick = async () => {
    const text = document.getElementById("transcriptBox").value;
    const language = document.getElementById("languageSelect").value;
    try {
        const response = await fetch("/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text, language: language }),
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById("translatedText").innerText = data.translation;
        } else {
            alert("Error in translation: " + data.error);
        }
    } catch (error) {
        console.error("Translation failed:", error);
    }
};

// Handle Speak Translation Button
document.getElementById("speakButton").onclick = async () => {
    const textToSpeak = document.getElementById("translatedText").innerText;
    try {
        const response = await fetch("/speak", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: textToSpeak }),
        });
        const data = await response.json();
        if (response.ok) {
            const audioElement = document.getElementById("audioPlayback");
            audioElement.src = data.audio_url;
            audioElement.play();
        } else {
            alert("Error in speech playback: " + data.error);
        }
    } catch (error) {
        console.error("Speech playback failed:", error);
    }
};
