
import importlib
import os


def _import_handler(module_path, handler_name="handler"):
    spec = importlib.util.spec_from_file_location("routes", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, handler_name)

def _create_route_from_file(app, file_path: str) -> None:
    parts = file_path.split(os.sep)
    method_file_result = parts[-1].split('.')[0].lower().split('__')
    
    last_route = method_file_result[0] if len(method_file_result) > 1 else None
    method = method_file_result[-1]
    
    route = os.sep.join(parts[:-1])
    route = route.replace('routes', '')
    route = route.replace('[', '{').replace(']', '}')
    route = '/' + route.strip(os.sep).replace(os.sep, "/") + "/" 
    
    if last_route:
        route += last_route
    
    handler = _import_handler(file_path)
    
    if method == "get":
        app.get(route)(handler)
    elif method == "post":
        app.post(route)(handler)
    elif method == "put":
        app.put(route)(handler)
    elif method == "delete":
        app.delete(route)(handler)
    elif method == "patch":
        app.patch(route)(handler)

def register_routes(app, base_path):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                _create_route_from_file(app, file_path)
