import logging
from typing import Optional, List, Dict

from deepgram import Deepgram
from pydantic import BaseModel

from domains.transcription.repository import TranscriptionClient, TranscriptionClientCredentials

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DeepgramAlternative(BaseModel):
    transcript: str
    confidence: float
    words: Optional[List[Dict]]


class DeepgramChannel(BaseModel):
    alternatives: List[DeepgramAlternative]


class DeepgramResult(BaseModel):
    channels: List[DeepgramChannel]


class DeepgramTranscriptionResult(BaseModel):
    metadata: dict
    results: DeepgramResult

    @property
    def get_result_unified(self) -> str:
        result_unified = ""
        for channel in self.results.channels:
            for alternative in channel.alternatives:
                result_unified = result_unified + alternative.transcript

        return result_unified


class DeepgramTranscriptionClientCredentials(TranscriptionClientCredentials):
    api_key: str


class DeepgramTranscriptionClient(TranscriptionClient):
    async def audio_to_text(self, media_url: str) -> str:
        if not media_url:
            raise ValueError("required media_url")

        logger.debug(f"credentials: {self._credentials} transcribe this: {media_url}")

        client = Deepgram(self._credentials.api_key)
        source = {"url": media_url}
        options = {"punctuate": True, "interim_results": True, "language": "es"}

        try:
            deepgram_res = await client.transcription.prerecorded(source, options)
        except Exception as e:
            logger.error(e)
            return ""

        print(f"Transcription complete!\n {deepgram_res}")

        deepgram_res = DeepgramTranscriptionResult.parse_obj(deepgram_res)

        return deepgram_res.get_result_unified


class DeepgramTranscriptionClientMock(TranscriptionClient):
    async def audio_to_text(self, media_url: str) -> str:
        return "This a text mock"
