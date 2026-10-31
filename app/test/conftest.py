import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from tortoise import Tortoise

from app.main import app


@pytest_asyncio.fixture
async def client():
    await Tortoise.init(
        db_url="sqlite://:memory:", modules={"models": ["app.models.model"]}
    )
    await Tortoise.generate_schemas()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    await Tortoise.close_connections()
