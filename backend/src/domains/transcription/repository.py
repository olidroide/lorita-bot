from abc import abstractmethod, ABC
from typing import ClassVar

from pydantic import BaseModel


class TranscriptionClientCredentials(BaseModel):
    pass


class TranscriptionClient(ABC):
    def __init__(self, credentials: ClassVar[TranscriptionClientCredentials]) -> None:
        self._credentials = credentials

    @abstractmethod
    async def audio_to_text(self, media_url: str) -> str:
        raise NotImplementedError
