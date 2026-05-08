from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
from routers.restaurant_api import restaurant_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(restaurant_api_router)
