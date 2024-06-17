from contextlib import asynccontextmanager
import logging
from urllib.parse import urlparse
from databases import Database


logger = logging.getLogger("SimplesAPI")


@asynccontextmanager
async def lifespan(app):
    await configure_database(app=app)
    app.cache = {}
    yield
    await close_database(app=app)


async def configure_database(app) -> Database:
    if app.simples.database_url:
        database_info = extract_db_info(app.simples.database_url)
        logger.info(
            f"Configuring database | Host: {database_info['host']} | Database: {database_info['database']}"
        )
        app.database = Database(app.simples.database_url)
        await app.database.connect()



def extract_db_info(db_url: str) -> dict:
    parsed_url = urlparse(db_url)
    host = parsed_url.hostname
    db_name = parsed_url.path.lstrip("/")  # Remove leading slash

    return {"host": host, "database": db_name}
async def close_database(app) -> Database:
    if app.database:
        database_info = extract_db_info(app.simples.database_url)
        logger.info(
            f"Closing database | Host: {database_info['host']} | Database: {database_info['database']}"
        )
        await app.database.close()

