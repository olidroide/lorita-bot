import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api_router import router as api_router
from app import get_settings
from robots_router import router as robots_router


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

    dir_path = os.path.dirname(os.path.realpath(__file__))
    app.mount("/", StaticFiles(directory=os.path.join(dir_path, "static")), name="static")

    # app.include_router(
    #     robots_router,
    #     tags=["robots"],
    # )

    app.include_router(
        api_router,
        prefix=app.state.config.baseurl,
        tags=["api"],
    )

    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=app.state.config.port)
