from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import PlainTextResponse

router = APIRouter()


@router.get("/robots.txt", response_class=PlainTextResponse)
async def whatsapp_receiver(request: Request):
    lines = [
        "User-Agent: *",
        "Disallow: /private/",
        "Disallow: /junk/",
    ]
    return "\n".join(lines)
