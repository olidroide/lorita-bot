from contextlib import asynccontextmanager
from typing import AsyncIterator

from app import get_settings
from .deepgram_transcription_client import (
    DeepgramTranscriptionClient,
    DeepgramTranscriptionClientCredentials,
    DeepgramTranscriptionClientMock,
)

config = get_settings()


@asynccontextmanager
async def get_deepgram_client(api_key: str) -> AsyncIterator[DeepgramTranscriptionClient]:
    if config.testing:
        yield DeepgramTranscriptionClientMock(credentials=DeepgramTranscriptionClientCredentials(api_key="testing"))
    else:
        yield DeepgramTranscriptionClient(credentials=DeepgramTranscriptionClientCredentials(api_key=api_key))
