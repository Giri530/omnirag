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
class SmartTranslator:
    def __init__(self):
        """Initialize translator for post-retrieval translation"""
        self.translator = None
        self.language_map = self._create_language_map()
        self._init_translator()
    def _create_language_map(self):
        return {
            'english': 'en', 'en': 'en',
            'tamil': 'ta', 'ta': 'ta',
            'hindi': 'hi', 'hi': 'hi',
            'telugu': 'te', 'te': 'te',
            'marathi': 'mr', 'mr': 'mr',
            'gujarati': 'gu', 'gu': 'gu',
            'kannada': 'kn', 'kn': 'kn',
            'malayalam': 'ml', 'ml': 'ml',
            'punjabi': 'pa', 'pa': 'pa',
            'bengali': 'bn', 'bn': 'bn',
            'spanish': 'es', 'es': 'es',
            'french': 'fr', 'fr': 'fr',
            'german': 'de', 'de': 'de',
            'italian': 'it', 'it': 'it',
            'portuguese': 'pt', 'pt': 'pt',
            'dutch': 'nl', 'nl': 'nl',
            'polish': 'pl', 'pl': 'pl',
            'russian': 'ru', 'ru': 'ru',
            'turkish': 'tr', 'tr': 'tr',
            'chinese': 'zh', 'zh': 'zh',
            'japanese': 'ja', 'ja': 'ja',
            'korean': 'ko', 'ko': 'ko',
            'vietnamese': 'vi', 'vi': 'vi',
            'thai': 'th', 'th': 'th',
            'indonesian': 'id', 'id': 'id',
            'malay': 'ms', 'ms': 'ms',
            'arabic': 'ar', 'ar': 'ar',
            'auto': 'auto', 'automatic': 'auto'
        }
    def normalize_language(self, language):
        if not language:
            return 'auto'
        lang_lower = str(language).lower().strip()
        return self.language_map.get(lang_lower, 'en')
    def _init_translator(self):
        try:
            from deep_translator import GoogleTranslator
            self.translator_type = "google"
            print("Smart Translator initialized (Google)")
        except ImportError:
            print("Install: pip install deep-translator")
            self.translator_type = "none"
    def detect_language(self, text):
        try:
            from langdetect import detect
            return detect(text)
        except:
            tamil_chars = any('\u0B80' <= c <= '\u0BFF' for c in text)
            hindi_chars = any('\u0900' <= c <= '\u097F' for c in text)
            if tamil_chars:
                return 'ta'
            elif hindi_chars:
                return 'hi'
            else:
                return 'en'
    def translate_answer(self, answer_text, source_chunks, target_language):
        """Translate final answer to target language"""
        if not answer_text:
            return answer_text
        target_lang = self.normalize_language(target_language)
        source_lang = self.detect_language(answer_text)
        if source_lang == target_lang:
            print(f"Already in {target_language}, no translation needed")
            return answer_text
        print(f"Translating: {source_lang} → {target_language} ({target_lang})")
        if self.translator_type == "google":
            return self._translate_google(answer_text, source_lang, target_lang)
        else:
            return answer_text
    def _translate_google(self, text, source, target):
        import time
        try:
            from deep_translator import GoogleTranslator
            if len(text) > 5000:
                sentences = text.split('. ')
                translated_parts = []
                for sentence in sentences:
                    for attempt in range(3):
                        try:
                            translator = GoogleTranslator(source=source, target=target)
                            translated = translator.translate(sentence)
                            translated_parts.append(translated)
                            break
                        except:
                            if attempt < 2:
                                time.sleep(1)
                                continue
                            else:
                                translated_parts.append(sentence)
                return '. '.join(translated_parts)
            else:
                for attempt in range(3):
                    try:
                        translator = GoogleTranslator(source=source, target=target)
                        return translator.translate(text)
                    except Exception as e:
                        if attempt < 2:
                            time.sleep(1)
                            continue
                        else:
                            print(f"Translation failed: {e}")
                            return text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    def get_supported_languages(self):
        return {
            'en': 'English', 'ta': 'Tamil', 'hi': 'Hindi',
            'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'zh': 'Chinese', 'ja': 'Japanese', 'ar': 'Arabic',
            'ru': 'Russian', 'pt': 'Portuguese', 'it': 'Italian',
            'ko': 'Korean', 'tr': 'Turkish', 'nl': 'Dutch',
            'pl': 'Polish', 'vi': 'Vietnamese', 'th': 'Thai',
            'id': 'Indonesian', 'ms': 'Malay', 'bn': 'Bengali',
            'te': 'Telugu', 'mr': 'Marathi', 'gu': 'Gujarati',
            'kn': 'Kannada', 'ml': 'Malayalam', 'pa': 'Punjabi'
        }
