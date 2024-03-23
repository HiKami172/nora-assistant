from elevenlabs.client import ElevenLabs
from elevenlabs import generate, play, Voice, VoiceSettings

import os
import logging
from typing import Union
from configuration import ConfigLoader

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class SpeechSynthesizer:
    """Preconfigured vocalization mechanism."""

    def __init__(self, model: str = None,
                 voice: Union[str, Voice] = None,
                 api_key: str = os.environ['ELEVEN_SECRET'],
                 config_path: str = None):
        if config_path is not None:
            logger.info('Config path provided. Loading config.')
            self.load_config(config_path)
            return
        self.model = model
        if api_key is None:
            logger.error('API key is required.')
            raise ValueError("API key is required.")
        self.client = ElevenLabs(api_key=api_key)
        self.voice = voice

    def synthesize_speech(self, text):
        """Say something using preconfigured voice settings of Elevenlabs API."""
        logger.info('Starting speech synthesis.')

        # TODO add voice streaming
        audio = generate(
            text=text,
            voice=self.voice,
            model=self.model,
        )
        play(audio)
        logger.info('Speech synthesis finished.')

    def load_config(self, config_path: str) -> None:
        """Loads preconfigured voice."""
        logger.info('Loading configuration from file.')
        config = ConfigLoader.load_yaml_file(config_path)
        model = config.get('model', 'eleven_multilingual_v2')
        voice_id = config.get('voice_id', 'Rachel')
        voice_settings = config.get('voice_settings', None)
        self.model = model
        self.voice = Voice(voice_id=voice_id)
        if voice_settings is not None:
            self.voice.settings = VoiceSettings(**voice_settings)
        logger.info('Configuration loaded successfully.')