# **Uni-Verse**

## Features

* **Text Translation:** Translate text between multiple languages using free services (Google via deep-translator, MyMemory, LibreTranslate).
* **Audio Input:** Supports speech-to-text conversion for audio files (offline transcription via Vosk if installed).
* **Slang & Proverb Handling:** Basic dictionary-based support for common slangs and proverbs.
* **Modular Design:** Clean, scalable architecture for easy upgrades.
* **Cross-Language Support:** English, Hindi, Marathi, Gujarati (expandable).
* **Optional Audio Output:** Plays translated text using TTS if dependencies are installed.

---

## File Structure

```
Uni-Verse/
├── main.py          # Core script handling text/audio input and translation
├── requirements.txt # Python dependencies
├── README.md        # Project documentation
├── slangs.json      # Slang/proverb dictionary for context-aware translation
└── sample_audio/    # Sample audio files for testing (contains .gitkeep placeholder for empty folder)
```

---

## Clone Repository

```bash
git clone https://github.com/Liar-Liar-28/Uni-Verse.git
cd Uni-Verse
```

---

## Installation

```bash
pip install -r requirements.txt
```

> ⚠️ Ensure `vosk` models are downloaded if you want offline audio transcription.
> PyAudio is required only if recording audio directly (not just using WAV files).

---

## Usage

### Text Input Translation

```bash
python main.py
```

* Enter your text when prompted.
* Select the target language code.

### Audio Input Translation (Optional)

* Place a `.wav` audio file in `sample_audio/`.
* Run the script and choose audio input mode for transcription and translation.

### Audio Output (Optional)

* After translation, you can choose to play the translated text via TTS.
* Works if `pyttsx3` is installed or system-level TTS is available.

---

## Sample Slangs Dictionary (`slangs.json`)

```json
{
  "brb": "be right back",
  "lol": "laughing out loud",
  "jaldi": "hurry up",
  "acha": "okay",
  "yaar": "friend"
}
```

---

## Current Functionality

* Translates plain text between multiple languages.
* Handles a small set of predefined slangs and proverbs.
* Supports audio input for speech-to-text conversion via Vosk.
* Optional audio playback of translated text via TTS.

---

## Future Roadmap

### Phase 1 – Expand Slang & Proverb Handling (2–4 weeks)

* Integrate AI-based slang detection.
* Fetch unknown slangs/proverbs dynamically via API or lightweight web scraping.
* Maintain a growing JSON dictionary automatically.

### Phase 2 – Audio Output & Conversational Translation (3–5 weeks)

* Enhance TTS for natural voice output.
* Implement multi-turn conversational translation mode.

### Phase 3 – Tone Detection & Context Awareness (4–6 weeks)

* Detect input tone (formal, casual, sarcastic, friendly) using NLP sentiment analysis.
* Adjust translations to preserve context and tone.
* Implement context memory for multi-turn dialogues.

### Phase 4 – Expanded Language Support (Ongoing)

* Gradually add regional and international languages.
* Ensure slang/proverb detection scales across languages.
* Maintain modular design for future upgrades.

### Phase 5 – Deployment & Optimization (Ongoing)

* Optimize for real-time performance.
* Deploy as a web or mobile app with cloud-based AI support.
* Continuously integrate new slang/proverb datasets and model updates.

---

## License

**MIT License**

Copyright (c) 2025 **Liar-Liar-28**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---
