#!/usr/bin/env python3
"""
Uni-Verse: Lean Multi-Language Translator
=========================================
A stable, minimal translation tool with core functionality:
- Text and audio (.wav only) input
- Multi-language translation via Google Translate
- Smart slang handling
- Text-to-speech output
- Clean error handling

Author: Your Name
Date: 2025
Version: 1.5 (Lean & Stable)
"""

import json
import os
import sys
import re
import signal
import tempfile
from typing import Optional, Dict

# Third-party imports with error handling
try:
    from googletrans import Translator, LANGUAGES
    import speech_recognition as sr
    from gtts import gTTS
    from playsound import playsound
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("📦 Install with: pip install googletrans==4.0.0rc1 SpeechRecognition gTTS playsound")
    sys.exit(1)


class UniVerseTranslator:
    """Lean translator with core functionality."""
    
    def __init__(self):
        """Initialize translator with minimal configuration."""
        self.slang_dict = self._load_slang_dictionary()
        self.translator = Translator()
        self.recognizer = sr.Recognizer()
        self.temp_files = []
        
        # Setup graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Core TTS supported languages (tested and stable)
        self.tts_supported = {
            'en', 'hi', 'mr', 'gu', 'es', 'fr', 'de', 'it', 'pt', 'ru',
            'ja', 'ko', 'zh', 'ar', 'tr', 'nl', 'pl', 'sv', 'da', 'no'
        }
    
    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        print("\n\n👋 Goodbye! Thanks for using Uni-Verse Translator!")
        self._cleanup_temp_files()
        sys.exit(0)
    
    def _cleanup_temp_files(self):
        """Clean up temporary files."""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass
        self.temp_files.clear()
    
    def _load_slang_dictionary(self) -> Dict[str, str]:
        """Load slang dictionary with simple error handling."""
        slang_file = "slangs.json"
        
        try:
            if not os.path.exists(slang_file):
                # Create default slang dictionary
                default_slangs = {
                    "gonna": "going to", "wanna": "want to", "y'all": "you all",
                    "ain't": "is not", "dunno": "don't know", "can't": "cannot",
                    "won't": "will not", "shouldn't": "should not",
                    "couldn't": "could not", "wouldn't": "would not",
                    "lemme": "let me", "gimme": "give me", "kinda": "kind of",
                    "sorta": "sort of", "gotta": "got to"
                }
                
                with open(slang_file, "w", encoding='utf-8') as f:
                    json.dump(default_slangs, f, indent=2, ensure_ascii=False)
                
                print(f"📝 Created {slang_file} with {len(default_slangs)} common slangs")
                return default_slangs
            
            with open(slang_file, "r", encoding='utf-8') as f:
                slang_dict = json.load(f)
                print(f"✅ Loaded {len(slang_dict)} slang entries")
                return slang_dict
                
        except json.JSONDecodeError:
            print("⚠️  Invalid JSON in slangs.json, using empty dictionary")
            return {}
        except Exception:
            print("⚠️  Could not load slangs.json, using empty dictionary")
            return {}
    
    def _clean_word_for_slang(self, word: str):
        """Clean word for slang matching, preserving punctuation."""
        # Handle basic punctuation
        match = re.match(r'^(\W*)(.*?)(\W*)$', word)
        if match:
            prefix, clean_word, suffix = match.groups()
            return prefix, clean_word.lower(), suffix
        return '', word.lower(), ''
    
    def handle_slangs(self, text: str) -> str:
        """Replace known slangs with clean handling."""
        if not text or not self.slang_dict:
            return text
        
        words = text.split()
        processed_words = []
        
        for word in words:
            prefix, clean_word, suffix = self._clean_word_for_slang(word)
            
            if clean_word in self.slang_dict:
                replacement = self.slang_dict[clean_word]
                processed_word = prefix + replacement + suffix
            else:
                processed_word = word
            
            processed_words.append(processed_word)
        
        return " ".join(processed_words)
    
    def audio_to_text(self, file_path: str) -> Optional[str]:
        """Convert WAV audio file to text."""
        try:
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                return None
            
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in ['.wav', '.wave']:
                print(f"❌ Unsupported audio format: {file_ext}")
                print("💡 Only .wav files are supported")
                return None
            
            print("🎤 Processing audio...")
            with sr.AudioFile(file_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.record(source)
                
            print("🧠 Recognizing speech...")
            text = self.recognizer.recognize_google(audio_data)
            print("✅ Speech recognition successful")
            return text
            
        except sr.UnknownValueError:
            print("❌ Could not understand the audio")
            print("💡 Try with clearer audio or check volume levels")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            print("💡 Check your internet connection")
            return None
        except Exception as e:
            print(f"❌ Audio processing error: {e}")
            return None
    
    def translate_text(self, text: str, dest_lang: str) -> Optional[str]:
        """Translate text to target language."""
        try:
            if not text.strip():
                print("❌ Empty text provided")
                return None
            
            # Process slangs
            processed_text = self.handle_slangs(text)
            if processed_text != text:
                print("🔄 Processed slangs in text")
            
            # Validate language code
            if dest_lang not in LANGUAGES:
                print(f"❌ Unsupported language code: '{dest_lang}'")
                self._show_language_suggestions()
                return None
            
            # Perform translation
            print(f"🌐 Translating to {LANGUAGES[dest_lang].title()}...")
            translated = self.translator.translate(processed_text, dest=dest_lang)
            
            if translated and translated.text:
                return translated.text
            else:
                print("❌ Translation returned empty result")
                return None
                
        except Exception as e:
            print(f"❌ Translation error: {e}")
            print("💡 Check your internet connection and try again")
            return None
    
    def text_to_speech(self, text: str, lang: str) -> bool:
        """Convert text to speech with simple handling."""
        try:
            if not text.strip():
                print("❌ Empty text for TTS")
                return False
            
            # Check TTS language support
            if lang not in self.tts_supported:
                print(f"🔇 TTS not available for language '{lang}'")
                print("🔇 Skipping audio output")
                return False
            
            print("🔊 Generating speech...")
            
            # Create temporary audio file
            temp_audio_fd, temp_audio = tempfile.mkstemp(suffix='.mp3')
            os.close(temp_audio_fd)
            self.temp_files.append(temp_audio)
            
            # Generate and play TTS
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_audio)
            
            print("▶️  Playing audio...")
            playsound(temp_audio)
            print("✅ Audio playback complete")
            return True
            
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
            print("🔇 Continuing without audio output")
            return False
    
    def _show_language_suggestions(self):
        """Display popular language codes."""
        popular_langs = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'hi': 'Hindi', 'mr': 'Marathi',
            'gu': 'Gujarati', 'zh': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean',
            'ar': 'Arabic', 'ru': 'Russian'
        }
        
        print("\n💡 Popular language codes:")
        for code, name in popular_langs.items():
            print(f"   {code} = {name}")
        print("   For complete list: https://cloud.google.com/translate/docs/languages")
    
    def _get_user_input_safe(self, prompt: str) -> str:
        """Get user input with error handling."""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            self._cleanup_temp_files()
            sys.exit(0)
    
    def _display_header(self):
        """Display application header."""
        print("=" * 55)
        print("🌍 UNI-VERSE TRANSLATOR 🌍")
        print("Lean Multi-Language Translation Tool")
        print("=" * 55)
        print("📋 Features:")
        print("   • Text & Audio (.wav) input")
        print("   • Smart slang handling")
        print("   • Text-to-speech output")
        print("   • 100+ language support")
        print()
        print("⚠️  Requirements:")
        print("   • Internet connection required")
        print("   • Only .wav files supported for audio")
        print("   • Press Ctrl+C to exit anytime")
        print("=" * 55)
    
    def _get_input_mode(self) -> str:
        """Get and validate input mode."""
        while True:
            print("\n📥 Input Options:")
            print("   1️⃣  Text input")
            print("   2️⃣  Audio file (.wav only)")
            
            mode = self._get_user_input_safe("Choose mode (1 or 2): ")
            
            if mode in ['1', '2']:
                return mode
            
            print("❌ Invalid selection. Please enter 1 or 2.")
    
    def _get_text_input(self) -> Optional[str]:
        """Get text input from user."""
        text = self._get_user_input_safe("📝 Enter text to translate: ")
        
        if not text:
            print("❌ No text entered")
            return None
        
        return text
    
    def _get_audio_input(self) -> Optional[str]:
        """Get audio input and convert to text."""
        while True:
            audio_path = self._get_user_input_safe("🎵 Enter path to WAV audio file: ")
            
            if not audio_path:
                print("❌ No file path entered")
                return None
            
            # Expand user path
            audio_path = os.path.expanduser(audio_path.strip('"\''))
            
            text = self.audio_to_text(audio_path)
            if text:
                print(f"✅ Recognized: '{text}'")
                return text
            
            retry = self._get_user_input_safe("❓ Try another file? (y/n): ").lower()
            if not retry.startswith('y'):
                return None
    
    def _get_target_language(self) -> Optional[str]:
        """Get and validate target language."""
        self._show_language_suggestions()
        
        while True:
            lang = self._get_user_input_safe("\n🌐 Enter target language code: ").lower()
            
            if not lang:
                print("❌ No language code entered")
                continue
            
            if lang in LANGUAGES:
                return lang
            
            print(f"❌ Invalid language code: '{lang}'")
            retry = self._get_user_input_safe("❓ Try again? (y/n): ").lower()
            if not retry.startswith('y'):
                return None
    
    def _display_results(self, original: str, translated: str, lang_code: str):
        """Display translation results."""
        lang_name = LANGUAGES.get(lang_code, lang_code).title()
        
        print(f"\n{'='*20} 📋 RESULTS {'='*20}")
        print(f"📤 Original:   {original}")
        print(f"📥 Translated: {translated}")
        print(f"🌐 Language:   {lang_name} ({lang_code})")
        print("=" * 50)
    
    def _offer_audio_output(self, text: str, lang: str):
        """Offer audio output to user."""
        if lang not in self.tts_supported:
            print(f"🔇 Audio output not available for language '{lang}'")
            return
        
        play_audio = self._get_user_input_safe("🔊 Play audio translation? (y/n): ").lower()
        
        if play_audio.startswith('y'):
            self.text_to_speech(text, lang)
    
    def run(self):
        """Main application loop."""
        try:
            # Display header
            self._display_header()
            
            # Get input mode
            mode = self._get_input_mode()
            
            # Get input text
            if mode == "1":
                input_text = self._get_text_input()
            else:  # mode == "2"
                input_text = self._get_audio_input()
            
            if not input_text:
                print("❌ No input provided. Exiting.")
                return
            
            # Get target language
            target_lang = self._get_target_language()
            if not target_lang:
                print("❌ No valid language selected. Exiting.")
                return
            
            # Perform translation
            translated_text = self.translate_text(input_text, target_lang)
            if not translated_text:
                print("❌ Translation failed. Exiting.")
                return
            
            # Display results
            self._display_results(input_text, translated_text, target_lang)
            
            # Offer audio output
            self._offer_audio_output(translated_text, target_lang)
            
            print("\n✅ Translation complete!")
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("💡 Please try again")
        
        finally:
            # Cleanup
            self._cleanup_temp_files()


def main():
    """Entry point for the lean application."""
    try:
        translator = UniVerseTranslator()
        translator.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
