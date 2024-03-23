from speech_synthesizer import SpeechSynthesizer
from recognition import Recognizer
from llm_processing import ModelAgent


class VoiceAssistant:
    """Utilizes recognition, LLM inference and TTS for user query processing."""

    def __init__(self):
        self.recognizer = Recognizer('ru-RU', 'configuration/google/service_credentials.json', 3)
        self.model = ModelAgent()
        self.vocalizer = SpeechSynthesizer()

    def _listen(self) -> str:
        """Recognizes user's audio input and returns it as a string."""
        return self.recognizer.run()

    def _process_query(self, query: str) -> str:
        """Processes user's query with agent chain and returns its response."""
        return self.model.process(query)

    def _say(self, text: str) -> None:
        """Says the provided text using ElevenLabs API."""
        self.vocalizer.synthesize_speech(text)

    def run(self, voice=False) -> str:
        """Listens for user audio input, processes it with llm agent and says its response."""
        query = self._listen()
        response = self._process_query(query)
        if voice:
            self._say(response)
        return response
