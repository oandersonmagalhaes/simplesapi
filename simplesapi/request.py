from typing import Any, Callable, Type, get_type_hints
from pydantic import BaseModel
from starlette.requests import HTTPConnection
from starlette.exceptions import HTTPException
import inspect

from simplesapi.types import Cache, Database


class SRequest:
    def __init__(self, route: str, handler: Callable, method: str, simples_extra: Any = None):
        self.handler = handler
        self.method = method
        self.route = route
        self.simples_extra = simples_extra
        self.injected_params = None
        self.handler_params = inspect.signature(self.handler).parameters.values()
        self.handle_param_names = [param.name for param in self.handler_params]

    def extract_route_params(self):
        """Extract route parameters from the route string"""
        parts = self.route.split("/")
        return [
            part[1:-1] for part in parts if part.startswith("{") and part.endswith("}")
        ]

    def inject_params(self, request: HTTPConnection, handler_params: list):
        if not self.injected_params:
            self.injected_params = {}
            if hasattr(request.app, "database"):
                [
                    self.injected_params.update(
                        {handle_param.name: request.app.database}
                    )
                    for handle_param in handler_params
                    if handle_param.annotation is Database
                ]
            if hasattr(request.app, "cache"):
                [
                    self.injected_params.update({handle_param.name: request.app.cache})
                    for handle_param in handler_params
                    if handle_param.annotation is Cache
                ]
    
    def get_param_type_by_name(self, function, param_name: str) -> Type:
        param_types = get_type_hints(function)
        return param_types.get(param_name)
    
    async def request(self, request: HTTPConnection):
        route_params = self.extract_route_params()
        request_params = request.path_params
        query_params = request.query_params

        self.inject_params(request, self.handler_params)

        path_params = {
            param: request.path_params[param]
            for param in route_params
            if param in request_params and param in self.handle_param_names
        }
        query_params = {
            param: request.query_params[param]
            for param in query_params
            if param not in request_params and param in self.handle_param_names
        }
        extra_params = {"_simples_extra": self.simples_extra} if "_simples_extra" in self.handle_param_names else {}
        
        missing_params = [
            param
            for param in self.handle_param_names
            if param not in path_params.keys()
            and param not in query_params.keys()
            and param not in self.injected_params.keys()
            and param not in ["_simples_extra"]
        ]

        models = {}

        if request.method in ["POST", "PUT", "PATCH"] and len(missing_params) == 1 and issubclass(self.get_param_type_by_name(self.handler, missing_params[0]), BaseModel):
            [
                models.update(
                    {handle_param.name: self.get_param_type_by_name(self.handler, handle_param.name)(**await request.json())}
                )
                for handle_param in self.handler_params
                if handle_param.name == missing_params[0]
            ]
            missing_params = []
            
        if missing_params:
            raise HTTPException(
                status_code=400, detail=f"Missing fields: {";".join(missing_params)}"
            )
        return await self.handler(**path_params, **self.injected_params, **query_params, **extra_params, **models)
