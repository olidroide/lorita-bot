from typing import Optional, List, Dict

from deepgram import Deepgram
from pydantic import BaseModel

from domains.transcription.repository import TranscriptionClient, TranscriptionClientCredentials


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
        client = Deepgram(self._credentials.api_key)
        source = {"url": media_url}
        options = {"punctuate": True, "interim_results": True, "language": "es"}

        deepgram_res = await client.transcription.prerecorded(source, options)

        print(f"Transcription complete!\n {deepgram_res}")

        deepgram_res = DeepgramTranscriptionResult.parse_obj(deepgram_res)

        return deepgram_res.get_result_unified


class DeepgramTranscriptionClientMock(TranscriptionClient):
    async def audio_to_text(self, media_url: str) -> str:
        return "This a text mock"
