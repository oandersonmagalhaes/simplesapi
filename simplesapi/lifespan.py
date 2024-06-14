from contextlib import asynccontextmanager

database = None

@asynccontextmanager
async def lifespan(app):
    app.database = {}
    app.cache = {}
    yield
