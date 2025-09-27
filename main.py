#!/usr/bin/env python3
"""
Uni-Verse: Ultra-Clean FREE Translator
======================================
Production-ready, 150-line free translator with all improvements
"""

import json
import os
import re
import subprocess
import platform
import requests
from typing import Optional, Dict

# Check dependencies
try:
    from deep_translator import GoogleTranslator
    import pyttsx3
except ImportError as e:
    print(f"Install: pip install deep-translator pyttsx3 requests")
    exit(1)

# Optional Vosk for offline transcription
try:
    import vosk
    import wave
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False


class UltraTranslator:
    def __init__(self):
        self.slang_dict = {
            "gonna": "going to", "wanna": "want to", "y'all": "you all",
            "ain't": "is not", "dunno": "don't know", "can't": "cannot",
            "won't": "will not", "lemme": "let me", "gimme": "give me",
            "kinda": "kind of", "sorta": "sort of", "gotta": "got to"
        }
        self.tts_engine = self._init_tts()
        self.vosk_model = None
        self.lang_shortcuts = {
            'es': 'Spanish', 'fr': 'French', 'de': 'German', 'hi': 'Hindi',
            'ja': 'Japanese', 'ko': 'Korean', 'zh': 'Chinese', 'ru': 'Russian'
        }
    
    def _init_tts(self) -> Optional[object]:
        """Initialize text-to-speech engine."""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            return engine
        except:
            return None
    
    def _load_vosk_model(self) -> Optional[object]:
        """Lazy load Vosk model for speech recognition."""
        if not VOSK_AVAILABLE or self.vosk_model is not None:
            return self.vosk_model
        
        model_paths = [
            "vosk-model-en-us-0.22", "vosk-model-small-en-us-0.15",
            "./models/vosk-model-en-us-0.22", "./vosk-model-small-en-us-0.15"
        ]
        
        for path in model_paths:
            if os.path.exists(path):
                try:
                    self.vosk_model = vosk.Model(path)
                    return self.vosk_model
                except:
                    continue
        return None
    
    def handle_slang(self, text: str) -> str:
        """Replace slang using regex for better accuracy."""
        if not text:
            return text
        
        pattern = re.compile(r'\b(' + '|'.join(self.slang_dict.keys()) + r')\b', re.IGNORECASE)
        return pattern.sub(lambda m: self.slang_dict[m.group(0).lower()], text)
    
    def detect_language(self, text: str) -> str:
        """Auto-detect source language."""
        try:
            detected = GoogleTranslator(source='auto', target='en').translate(text)
            return GoogleTranslator().detect(text)
        except:
            return 'en'
    
    def translate(self, text: str, target_lang: str, source_lang: str = 'auto') -> Optional[str]:
        """Multi-service translation with fallback."""
        text = self.handle_slang(text)
        
        # Service 1: Google via deep-translator
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            result = translator.translate(text)
            if result and result.strip():
                return result.strip()
        except Exception as e:
            print(f"⚠️ Google failed: {str(e)[:50]}...")
        
        # Service 2: MyMemory API
        try:
            url = "https://api.mymemory.translated.net/get"
            params = {'q': text, 'langpair': f'{source_lang}|{target_lang}'}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('responseStatus') == 200:
                result = data['responseData']['translatedText']
                if result and result.strip():
                    return result.strip()
        except Exception as e:
            print(f"⚠️ MyMemory failed: {str(e)[:50]}...")
        
        # Service 3: LibreTranslate instances
        for instance in ["https://libretranslate.de", "https://translate.argosopentech.com"]:
            try:
                response = requests.post(f"{instance}/translate", 
                                       data={'q': text, 'source': source_lang, 'target': target_lang},
                                       timeout=10)
                result = response.json().get('translatedText')
                if result and result.strip():
                    return result.strip()
            except:
                continue
        
        return None
    
    def speak(self, text: str, lang: str = 'en') -> bool:
        """Cross-platform text-to-speech."""
        if not text:
            return False
        
        # Escape text for shell safety
        safe_text = text.replace('"', '\\"').replace("'", "\\'")
        
        # Try pyttsx3 first
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return True
            except:
                pass
        
        # System-level fallbacks
        system = platform.system().lower()
        try:
            if system == "windows":
                cmd = f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{safe_text}\')"'
                subprocess.run(cmd, shell=True, timeout=30)
                return True
            elif system == "darwin":
                subprocess.run(['say', text], timeout=30)
                return True
            elif system == "linux":
                if os.system("which espeak > /dev/null 2>&1") == 0:
                    subprocess.run(['espeak', text], timeout=30)
                    return True
        except:
            pass
        
        print("⚠️ Text-to-speech not available")
        return False
    
    def transcribe_audio(self, audio_file: str) -> Optional[str]:
        """Offline speech recognition with Vosk."""
        model = self._load_vosk_model()
        if not model:
            print("⚠️ Vosk model not found. Download from: https://alphacephei.com/vosk/models/")
            return None
        
        try:
            with wave.open(audio_file, 'rb') as wf:
                rec = vosk.KaldiRecognizer(model, wf.getframerate())
                text = ""
                
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text += result.get('text', '') + " "
                
                final_result = json.loads(rec.FinalResult())
                text += final_result.get('text', '')
                
                return text.strip() if text.strip() else None
        except Exception as e:
            print(f"❌ Audio transcription failed: {e}")
            return None
    
    def get_input_text(self) -> Optional[str]:
        """Get text input via typing or audio file."""
        mode = input("Input mode (1=Type, 2=Audio file): ").strip()
        
        if mode == '1':
            text = input("Enter text: ").strip()
            return text if text else None
        
        elif mode == '2':
            audio_file = input("WAV file path: ").strip()
            if not os.path.exists(audio_file):
                print(f"❌ File not found: {audio_file}")
                return None
            
            print("🎤 Transcribing...")
            return self.transcribe_audio(audio_file)
        
        else:
            print("❌ Invalid mode")
            return None
    
    def get_target_language(self) -> Optional[str]:
        """Get target language with shortcuts."""
        print("Common: es=Spanish, fr=French, de=German, hi=Hindi, ja=Japanese")
        lang = input("Target language code: ").strip().lower()
        
        if lang in self.lang_shortcuts:
            print(f"🌐 Translating to {self.lang_shortcuts[lang]}")
        
        return lang if lang else None
    
    def run_session(self) -> bool:
        """Single translation session."""
        # Get input
        text = self.get_input_text()
        if not text:
            return True  # Continue loop
        
        print(f"📝 Input: {text}")
        
        # Get target language
        target_lang = self.get_target_language()
        if not target_lang:
            return True
        
        # Translate
        print("🔄 Translating...")
        translated = self.translate(text, target_lang)
        
        if not translated:
            print("❌ All translation services failed")
            return True
        
        # Display results
        print(f"🌐 Translation: {translated}")
        
        # Optional audio
        if input("🔊 Play audio? (y/n): ").strip().lower().startswith('y'):
            self.speak(translated, target_lang)
        
        return True
    
    def run(self):
        """Main application loop."""
        print("🌍 ULTRA-CLEAN FREE TRANSLATOR 🌍")
        print("=" * 45)
        
        while True:
            try:
                if not self.run_session():
                    break
                
                if not input("\n↻ Translate more? (Enter=yes, 'q'=quit): ").strip().lower() != 'q':
                    break
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
        
        print("Thanks for using Ultra Translator!")


if __name__ == "__main__":
    app = UltraTranslator()
    app.run()
