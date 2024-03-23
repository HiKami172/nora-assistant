import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)
config = {}


class Recognizer:
    """Recognizes user's voice using Google Speech."""
    def __init__(self, language: str, credentials: str, timeout: int):
        self.language = language
        self.credentials = credentials
        self.timeout = timeout
        self.recognizer = sr.Recognizer()

    def _listen(self) -> sr.AudioData:
        """Takes audio input from the user."""
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=self.timeout)
                return audio
            except sr.WaitTimeoutError as e:
                logger.error(f"Audio input timeout. {e}")

    def _recognize_speech(self, audio: sr.AudioData) -> str:
        """Recognizes the audio using Google Speech Recognition."""
        try:
            text = self.recognizer.recognize_google_cloud(audio, language=self.language,
                                                          credentials_json=self.credentials)
            logger.info(f"Recognized Text: {text}")
            return text
        except (sr.UnknownValueError, sr.RequestError) as e:
            logger.exception("Error occurred during speech recognition.", exc_info=e)
            raise

    def run(self) -> str:
        """Starts listening for audio from the user and returns recognized text."""
        logger.info("Listening...")
        audio = self._listen()
        logger.info("Recognizing...")
        text = self._recognize_speech(audio)
        return text


if __name__ == '__main__':
    recognizer = Recognizer('en-US', './secrets/service_credentials.json', 3)
    recognized_text = recognizer.run()
    print(recognized_text)
