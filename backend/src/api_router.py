import asyncio
from typing import Optional, ClassVar

from fastapi import APIRouter
from fastapi import Depends, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from app import get_settings, Settings
from domains.transcription.factory import get_deepgram_client
from domains.transcription.repository import TranscriptionClient

router = APIRouter()


class TwilioWhatsappReceiver(BaseModel):
    SmsMessageSid: Optional[str]
    NumMedia: Optional[int] = 0
    ProfileName: Optional[str]
    SmsSid: Optional[str]
    WaId: Optional[str]
    Body: Optional[str] = ""
    To: Optional[str]
    NumSegments: Optional[str]
    MessageSid: Optional[str]
    AccountSid: Optional[str]
    From: Optional[str]
    ApiVersion: Optional[str]

    def _get_dynamic_attr(self, name: str) -> Optional[str]:
        try:
            return getattr(self, name)
        except AttributeError:
            pass

    def get_media_url(self, id: int) -> Optional[str]:
        return self._get_dynamic_attr(f"MediaUrl{id}")

    def get_media_content_type(self, id: int) -> Optional[str]:
        return self._get_dynamic_attr(f"MediaContentType{id}")

    class Config:
        extra = "allow"


async def _process_twilio_media(
    receiver: TwilioWhatsappReceiver, media_id: int, transcription_client: ClassVar[TranscriptionClient]
):
    if not (media_url := receiver.get_media_url(media_id)):
        return

    if not (media_content_type := receiver.get_media_content_type(media_id)):
        return

    print(f"url: {media_url} content_type: {media_content_type}")

    if "audio" not in media_content_type:
        return

    return await transcription_client.audio_to_text(media_url=media_url)


async def proces_twilio_request(request_body: dict, transcription_client: ClassVar[TranscriptionClient]):
    receiver = TwilioWhatsappReceiver.parse_obj(request_body)
    if not (
        responses := await asyncio.gather(
            *[
                _process_twilio_media(receiver, media_item_counter, transcription_client)
                for media_item_counter in range(receiver.NumMedia)
            ]
        )
    ):
        responses = [receiver.Body]

    twilio_character_limit = 1600
    return "".join(responses)[:twilio_character_limit]


class MessageBirdContact(BaseModel):
    id: Optional[str]
    href: Optional[str]
    msisdn: Optional[int]
    displayName: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    customDetails: Optional[dict]
    attributes: Optional[dict]
    createdDatetime: Optional[str]
    updatedDatetime: Optional[str]


class MessageBirdConversationMessage(BaseModel):
    totalCount: Optional[int]
    href: Optional[str]


class MessageBirdConversation(BaseModel):
    id: Optional[str]
    contactId: Optional[str]
    status: Optional[str]
    createdDatetime: Optional[str]
    updatedDatetime: Optional[str]
    lastReceivedDatetime: Optional[str]
    lastUsedChannelId: Optional[str]
    messages: Optional[MessageBirdConversationMessage]


class MessageBirdMessageContentAudio(BaseModel):
    url: str


class MessageBirdMessageContent(BaseModel):
    audio: Optional[MessageBirdMessageContentAudio]
    text: Optional[str]


class MessageBirdMessage(BaseModel):
    id: Optional[str]
    conversationId: Optional[str]
    platform: Optional[str]
    to: Optional[str]
    from_: Optional[str]
    channelId: Optional[str]
    type: Optional[str]
    direction: Optional[str]
    status: Optional[str]
    createdDatetime: Optional[str]
    updatedDatetime: Optional[str]
    content: Optional[MessageBirdMessageContent]

    class Config:
        allow_population_by_field_name = True
        fields = {"from_": "from"}


class MessageBirdWhatsappReceiver(BaseModel):
    contact: Optional[MessageBirdContact]
    conversation: Optional[MessageBirdConversation]
    message: Optional[MessageBirdMessage]
    type: str


@router.post("/whatsapp/receive", response_class=PlainTextResponse)
async def whatsapp_receiver(request: Request, settings: Settings = Depends(get_settings)):
    incoming_msg = await request.form()
    final_dict = dict()
    for key, value in incoming_msg.items():
        final_dict[key] = value

    print(f"Request from: {request.headers} - {request.client} - {request.client.host}")

    # if "messagebird-signature" in request.headers:
    #     'user-agent': 'MessageBirdHTTPQueue/xxxxx'
    #  'user-agent': 'TwilioProxy/1.1',
    # 'x-twilio-signature'
    # TODO add request verification from Twilio or MessageBird
    async with get_deepgram_client(api_key=settings.dg_key) as transcription_client:
        transcribed_text = await proces_twilio_request(
            request_body=final_dict, transcription_client=transcription_client
        )

    return transcribed_text
