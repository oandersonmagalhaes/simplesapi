from typing import Any, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

from simplesapi import lifespan, settings
from simplesapi.auto_routing import register_routes


from simplesapi.internal_logger import simplesapi_internal_logger

class SimplesConfig(BaseModel):
    verbose: Optional[bool] = Field(default=False)
    base_path: Optional[str] = Field(default="/")
    routes_path: Optional[str] = Field(default="routes")
    cache_url: Optional[str] = Field(default=None)
    cache_ssl: Optional[bool] = Field(default=None)
    database_url: Optional[str] = Field(default=None)
    
    aws_local: Optional[bool] = Field(default=False)
    aws_access_key_id: Optional[str] = Field(default=None)
    aws_secret_access_key: Optional[str] = Field(default=None)
    aws_region_name: Optional[str] = Field(default=None)


class SimplesAPI(FastAPI):
    def __init__(
        self, routes_path=None, 
        cache_url=settings.SIMPLESAPI_CACHE_URL, 
        cache_ssl=settings.SIMPLESAPI_CACHE_SSL, 
        database_url=settings.SIMPLES_DABASE_URL, 
        aws_access_key_id=settings.SIMPLES_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.SIMPLES_AWS_SECRET_ACCESS_KEY,
        aws_region_name=settings.SIMPLES_AWS_REGION_NAME,
        aws_local=settings.SIMPLES_AWS_LOCAL,
        *args, **kwargs
    ):
        simplesapi_internal_logger()
        self.simples = SimplesConfig(
            routes_path=routes_path, 
            cache_url=cache_url, 
            cache_ssl=cache_ssl, 
            database_url=database_url, 
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_region_name=aws_region_name,
            aws_local=aws_local,
            **kwargs
        )
        super().__init__(lifespan=lifespan.lifespan, *args, **kwargs)
        if self.simples.routes_path:
            register_routes(self, self.simples.routes_path)
