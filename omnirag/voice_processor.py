import sys
import io
if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        else:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except:
        pass
class VoiceProcessor:
    def __init__(self):
        self.recognizer = None
        self.tts_engine = None
        self._init_voice()  
    def _init_voice(self):
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            print("Voice Input enabled (SpeechRecognition)")
        except ImportError:
            print(" Install: pip install SpeechRecognition pyaudio")
            self.recognizer = None
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150) 
            self.tts_engine.setProperty('volume', 0.9) 
            print("Voice Output enabled (pyttsx3)")
        except ImportError:
            print(" Install: pip install pyttsx3")
            self.tts_engine = None
    def listen(self, timeout=5, phrase_time_limit=10):
        if not self.recognizer:
            print(" Voice input not available")
            return None
        try:
            import speech_recognition as sr
            print("Listening... (speak now)")
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print(" No speech detected (timeout)")
            return None
        except sr.UnknownValueError:
            print(" Could not understand speech")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    def speak(self, text, language='en'):
        if not self.tts_engine:
            print("Voice output not available")
            print(f"Text: {text}")
            return
        try:
            try:
                print(f"Speaking: {text[:50]}...")
            except (UnicodeEncodeError, UnicodeDecodeError):
                print(f"Speaking answer...")
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if language in voice.id.lower() or language in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            print("Speech complete")
        except Exception as e:
            print(f" Speech error: {e}")
            try:
                print(f"Text: {text}")
            except:
                print("Text: [Special characters]")
    def set_voice_properties(self, rate=None, volume=None):
        if not self.tts_engine:
            return
        if rate:
            self.tts_engine.setProperty('rate', rate)
        if volume:
            self.tts_engine.setProperty('volume', volume)
    def list_available_voices(self):
        if not self.tts_engine:
            print(" TTS not available")
            return []
        voices = self.tts_engine.getProperty('voices')
        print("\n Available voices:")
        for i, voice in enumerate(voices):
            try:
                print(f"{i+1}. {voice.name} ({voice.id})")
                print(f"   Languages: {voice.languages}")
            except (UnicodeEncodeError, UnicodeDecodeError):
                print(f"{i+1}. Voice {i+1}")
        return voices
    def voice_conversation(self, query_callback, max_turns=5):
        for turn in range(max_turns):
            user_query = self.listen()
            if not user_query:
                continue
            if user_query.lower() in ['exit', 'quit', 'stop', 'bye']:
                self.speak("Goodbye!")
                break
            result = query_callback(user_query)
            if isinstance(result, dict):
                answer = result.get('answer', str(result))
            else:
                answer = str(result)
            self.speak(answer)
            print() 
