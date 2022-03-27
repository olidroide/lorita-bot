from typing import Optional, List, Dict

from deepgram import Deepgram
from fastapi import APIRouter
from fastapi import Depends, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from twilio.rest import Client  # type: ignore

from app import get_settings, Settings

router = APIRouter()


class TranscribeRequest(BaseModel):
    audio_url: str


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


async def audio_to_text(media_url: str) -> str:
    # submit the recording to deepgram
    client = Deepgram(get_settings().dg_key)
    source = {"url": media_url}
    options = {"punctuate": True, "interim_results": True, "language": "es"}

    deepgram_res = await client.transcription.prerecorded(source, options)

    print(f"Transcription complete!\n {deepgram_res}")

    deepgram_res = DeepgramTranscriptionResult.parse_obj(deepgram_res)

    return deepgram_res.get_result_unified


@router.post("/transcribe")
async def transcribe(data: TranscribeRequest, settings: Settings = Depends(get_settings)):
    print(f"got request in transcribe:{data.audio_url}")
    print(f"Settings: {settings}")
    print("sending recording to deepgram")

    result = await audio_to_text(media_url=data.audio_url)
    print("done processing request, sending deepgram response back to client", result)
    return result


class WhatsappReceiver(BaseModel):
    SmsMessageSid: Optional[str]
    NumMedia: Optional[int]
    ProfileName: Optional[str]
    SmsSid: Optional[str]
    WaId: Optional[str]
    Body: Optional[str]
    To: Optional[str]
    NumSegments: Optional[str]
    MessageSid: Optional[str]
    AccountSid: Optional[str]
    From: Optional[str]
    ApiVersion: Optional[str]


@router.post("/whatsapp/receive", response_class=PlainTextResponse)
async def whatsapp_receiver(request: Request, settings: Settings = Depends(get_settings)):
    incoming_msg = await request.form()
    final_dict = dict()
    for key, value in incoming_msg.items():
        final_dict[key] = value

    receiver = WhatsappReceiver.parse_obj(final_dict)
    print(f"got request : {receiver}")

    response = ""

    media_item_counter = 0
    while media_item_counter < receiver.NumMedia:
        media_url = final_dict[f"MediaUrl{media_item_counter}"]
        media_content_type = final_dict[f"MediaContentType{media_item_counter}"]
        print(f"url: {media_url} content_type: {media_content_type}")
        media_item_counter = media_item_counter + 1
        if "audio" in media_content_type:
            audio_text = await audio_to_text(media_url=media_url)
            response = response + audio_text

    if not response:
        response = receiver.Body

    return response
