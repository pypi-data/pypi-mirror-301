import asyncio
import logging
import sys

from pyflowery.models import FloweryAPIConfig
from pyflowery.pyflowery import FloweryAPI

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

api = FloweryAPI(FloweryAPIConfig(user_agent="PyFloweryTests"))

ALEXANDER = "fa3ea565-121f-5efd-b4e9-59895c77df23" # TikTok
JACOB = "38f45366-68e8-5d39-b1ef-3fd4eeb61cdb" # Microsoft Azure
STORMTROOPER = "191c5adc-a092-5eea-b4ff-ce01f66153ae" # TikTok

async def test_fetch_tts():
    """Test the fetch_tts method"""
    voice = api.get_voices(voice_id=ALEXANDER)[0]
    tts = await api.fetch_tts(text="Sphinx of black quartz, judge my vow. The quick brown fox jumps over a lazy dog.", voice=voice)
    try:
        with open('test.mp3', 'wb') as f:
            f.write(tts)
    except Exception as e: # pylint: disable=broad-except
        api.config.logger.error(e, exc_info=True)
    long_string = 'a' * 2049
    try:
        await api.fetch_tts(text=long_string)
    except ValueError as e:
        api.config.logger.error("This is expected to fail:\n%s", e, exc_info=True)

if __name__ == '__main__':
    api.config.logger.info("testing fetch_tts")
    asyncio.run(test_fetch_tts())
