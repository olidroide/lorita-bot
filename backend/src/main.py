import uvicorn
from fastapi import FastAPI
from twilio.rest import Client  # type: ignore
from twilio.rest import Client  # type: ignore

from api_router import router as api_router
from app import get_settings


def create_app():
    config = get_settings()

    app = FastAPI(
        title="⚡ LORITA BOT",
        description="Lorita is like a parrot instead repeat and audio, transcribe it to text",
        version="1.0.0",
        debug=config.debug,
        docs_url="/docs/",
        openapi_url="/docs/openapi.json",
        # servers=[{"url": config.baseurl}],
    )

    app.state.config = config

    @app.on_event("startup")
    async def startup_event():
        pass

    @app.on_event("shutdown")
    async def shutdown_event():
        pass

    app.include_router(
        api_router,
        prefix=app.state.config.baseurl,
        tags=["api"],
    )

    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=app.state.config.port)
