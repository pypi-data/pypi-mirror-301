import asyncio
from typing import AsyncGenerator, Tuple

from pyflowery.models import FloweryAPIConfig, Language, Voice
from pyflowery.rest_adapter import RestAdapter


class FloweryAPI:
    """Main class for interacting with the Flowery API

    Attributes:
        config (FloweryAPIConfig): Configuration object for the API
        adapter (RestAdapter): Adapter for making HTTP requests
    """
    def __init__(self, config: FloweryAPIConfig):
        self.config = config
        self.adapter = RestAdapter(config)
        self._voices_cache: Tuple[Voice] = ()
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            self.config.logger.info("Async event loop is already running. Adding `_populate_voices_cache()` to the event loop.")
            asyncio.create_task(self._populate_voices_cache())
        else:
            asyncio.run(self._populate_voices_cache())

    async def _populate_voices_cache(self):
        """Populate the voices cache. This method is called automatically when the FloweryAPI object is created, and should not be called directly."""
        self._voices_cache = tuple([voice async for voice in self.fetch_voices()]) # pylint: disable=consider-using-generator
        self.config.logger.info('Voices cache populated!')

    def get_voices(self, voice_id: str | None = None, name: str | None = None) -> Tuple[Voice] | None:
        """Get a set of voices from the cache.

        Args:
            voice_id (str): The ID of the voice
            name (str): The name of the voice

        Returns:
            Tuple[Voice] | None: A tuple of Voice objects if found, otherwise None
        """
        if voice_id:
            voice = next((voice for voice in self._voices_cache if voice.id == voice_id))
            return (voice,) or None
        if name:
            voices = []
            for voice in self._voices_cache:
                if voice.name == name:
                    voices.append(voice)
            return tuple(voices) or None
        return self._voices_cache or None

    async def fetch_voice(self, voice_id: str) -> Voice:
        """Fetch a voice from the Flowery API. This method bypasses the cache and directly queries the Flowery API. You should usually use `get_voice()` instead.

        Args:
            voice_id (str): The ID of the voice

        Raises:
            ValueError: Raised when the voice is not found
            TooManyRequests: Raised when the Flowery API returns a 429 status code
            ClientError: Raised when the Flowery API returns a 4xx status code
            InternalServerError: Raised when the Flowery API returns a 5xx status code
            RetryLimitExceeded: Raised when the retry limit defined in the `FloweryAPIConfig` class (default 3) is exceeded

        Returns:
            Voice: The voice
        """
        async for voice in self.fetch_voices():
            if voice.id == voice_id:
                return voice
        raise ValueError(f'Voice with ID {voice_id} not found.')

    async def fetch_voices(self) -> AsyncGenerator[Voice, None]:
        """Fetch a list of voices from the Flowery API

        Raises:
            TooManyRequests: Raised when the Flowery API returns a 429 status code
            ClientError: Raised when the Flowery API returns a 4xx status code
            InternalServerError: Raised when the Flowery API returns a 5xx status code
            RetryLimitExceeded: Raised when the retry limit defined in the `FloweryAPIConfig` class (default 3) is exceeded

        Returns:
            AsyncGenerator[Voice, None]: A generator of Voices
        """
        request = await self.adapter.get('/tts/voices')
        for voice in request.data['voices']:
            yield Voice(
                id=voice['id'],
                name=voice['name'],
                gender=voice['gender'],
                source=voice['source'],
                language=Language(**voice['language']),
            )

    async def fetch_tts(self, text: str, voice: Voice | str | None = None, translate: bool = False, silence: int = 0, audio_format: str = 'mp3', speed: float = 1.0) -> bytes:
        """Fetch a TTS audio file from the Flowery API

        Args:
            text (str): The text to convert to speech
            voice (Voice | str): The voice to use for the speech
            translate (bool): Whether to translate the text
            silence (int): Number of seconds of silence to add to the end of the audio
            audio_format (str): The audio format to return
            speed (float): The speed of the speech

        Raises:
            ValueError: Raised when the provided text is too long and `allow_truncation` in the `FloweryAPIConfig` class is set to `False` (default).
            TooManyRequests: Raised when the Flowery API returns a 429 status code
            ClientError: Raised when the Flowery API returns a 4xx status code
            InternalServerError: Raised when the Flowery API returns a 5xx status code
            RetryLimitExceeded: Raised when the retry limit defined in the `FloweryAPIConfig` class (default 3) is exceeded

        Returns:
            bytes: The audio file in bytes
        """
        if len(text) > 2048:
            if not self.config.allow_truncation:
                raise ValueError('Text must be less than or equal to 2048 characters')
            self.config.logger.warning('Text is too long, will be truncated to 2048 characters by the API')
        params = {
            'text': text,
            'translate': str(translate).lower(),
            'silence': silence,
            'audio_format': audio_format,
            'speed': speed,
        }
        if voice:
            params['voice'] = voice.id if isinstance(voice, Voice) else voice
        request = await self.adapter.get('/tts', params, timeout=180)
        return request.data
