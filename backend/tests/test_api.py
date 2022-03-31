import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

pytestmark = pytest.mark.asyncio


async def test_send_empty_body(
    initapp: FastAPI,
    client: AsyncClient,
):
    response = await client.post(url="/whatsapp/receive")
    assert response.status_code == HTTP_200_OK
