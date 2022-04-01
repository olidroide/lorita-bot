import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from src.main import create_app

app = create_app()


@pytest.fixture(scope="function")
async def application() -> FastAPI:
    try:
        app.state.config.testing = True
        yield app
    finally:
        pass


@pytest.fixture(scope="function")
async def initapp(application: FastAPI) -> FastAPI:
    async with LifespanManager(application):
        yield application


@pytest.fixture(scope="function")
async def client(initapp: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initapp,
        base_url=f"http://testserver{app.state.config.baseurl}",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
