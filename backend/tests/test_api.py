import asynctest
import pytest
from aiogram import types
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

from api_router import TwilioWhatsappReceiver

pytestmark = pytest.mark.asyncio


async def test_whatsapp_receive_empty_body(
    initapp: FastAPI,
    client: AsyncClient,
):
    response = await client.post(url="/whatsapp/receive")
    assert response.status_code == HTTP_200_OK
    assert response.text == ""


async def test_whatsapp_receive_twilio_audio_message(
    initapp: FastAPI,
    client: AsyncClient,
):
    twilio_whatsapp_receiver = TwilioWhatsappReceiver(
        SmsMessageSid="xxxxxxx",
        NumMedia=1,
        ProfileName="xxxx",
        SmsSid="xxxxx",
        WaId="666555444",
        Body=None,
        To="whatsapp:+199988877",
        NumSegments="1",
        MessageSid="xxxxxxx",
        AccountSid="yyyyy",
        From="whatsapp:+34666555444",
        ApiVersion="2010-04-01",
        MediaUrl0="https://api.twilio.com/2010-04-01/Accounts/yyyyy/Messages/xxxxxxx/Media/xxxxxxx",
        MediaContentType0="audio/ogg",
    )
    body = twilio_whatsapp_receiver.dict()

    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = await client.post(
        url="/whatsapp/receive",
        headers=headers,
        data=body,
    )
    assert response.status_code == HTTP_200_OK
    assert response.text == "This a text mock"


async def test_whatsapp_receive_twilio_body_without_audio(
    initapp: FastAPI,
    client: AsyncClient,
):
    expected_result = "hello world"
    twilio_whatsapp_receiver = TwilioWhatsappReceiver(
        SmsMessageSid="xxxxxxx",
        NumMedia=0,
        ProfileName="xxxx",
        SmsSid="xxxxx",
        WaId="666555444",
        Body=expected_result,
        To="whatsapp:+199988877",
        NumSegments="1",
        MessageSid="xxxxxxx",
        AccountSid="yyyyy",
        From="whatsapp:+34666555444",
        ApiVersion="2010-04-01",
    )
    body = twilio_whatsapp_receiver.dict()

    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = await client.post(
        url="/whatsapp/receive",
        headers=headers,
        data=body,
    )
    assert response.status_code == HTTP_200_OK
    assert response.text == expected_result


@asynctest.patch("aiogram.types.mixins.Downloadable.get_url", autospec=True)
async def test_webhook_telegram_receive_message(
    mock_aiogram_get_url,
    initapp: FastAPI,
    client: AsyncClient,
):
    mock_aiogram_get_url.return_value = "https://0.0.0.0/test.ogg"

    body = types.Update(
        **{
            "update_id": 666,
            "message": {
                "message_id": 1,
                "from": {
                    "id": 666,
                    "is_bot": False,
                    "first_name": "Oli",
                    "username": "olidroide",
                    "language_code": "es",
                },
                "chat": {"id": 666, "first_name": "Oli", "username": "olidroide", "type": "private"},
                "date": 1649250839,
                "voice": {
                    "duration": 2,
                    "mime_type": "audio/ogg",
                    "file_id": "xxxxx",
                    "file_unique_id": "xxxx",
                    "file_size": 12556,
                },
            },
        }
    ).to_python()

    response = await client.post(
        url="/telegram",
        json=body,
    )
    assert response.status_code == HTTP_200_OK
