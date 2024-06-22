import unittest
from unittest.mock import MagicMock, patch, call
from simplesapi.auto_routing import _import_handler, _create_route_from_file, register_routes
import os

class TestRoutes(unittest.TestCase):

    @patch('importlib.util.spec_from_file_location')
    @patch('importlib.util.module_from_spec')
    def test_import_handler(self, mock_module_from_spec, mock_spec_from_file_location):
        mock_spec = MagicMock()
        mock_module = MagicMock()
        mock_spec_from_file_location.return_value = mock_spec
        mock_module_from_spec.return_value = mock_module
        
        handler_name = 'handler'
        expected_handler = MagicMock()
        setattr(mock_module, handler_name, expected_handler)
        
        module_path = 'path/to/module.py'
        
        handler = _import_handler(module_path, handler_name)
        
        mock_spec.loader.exec_module.assert_called_once_with(mock_module)
        self.assertEqual(handler, expected_handler)
    
    @patch('simplesapi.auto_routing._import_handler')
    def test_create_route_from_file(self, mock_import_handler):
        app = MagicMock()
        handler = MagicMock()
        mock_import_handler.return_value = handler
        
        base_path = 'routes'
        file_path = os.path.join(base_path, 'api', 'v1', 'resource__get.py')
        _create_route_from_file(app, file_path, base_path)
        
        route = '/api/v1/resource'
        app.add_api_route.assert_called_once_with(route, handler, methods=['GET'])
    
    @patch('simplesapi.auto_routing._import_handler')
    def test_create_route_from_file_only_method(self, mock_import_handler):
        app = MagicMock()
        handler = MagicMock()
        mock_import_handler.return_value = handler
        
        base_path = 'routes'
        file_path = os.path.join('routes', 'api', 'v1', 'get.py')
        _create_route_from_file(app, file_path, base_path)
        
        route = '/api/v1/'
        app.add_api_route.assert_called_once_with(route, handler, methods=['GET'])
    
    @patch('os.walk')
    @patch('simplesapi.auto_routing._create_route_from_file')
    def test_register_routes(self, mock_create_route_from_file, mock_os_walk):
        app = MagicMock()
        base_path = 'base/path'
        
        mock_os_walk.return_value = [
            (base_path, ['dir'], ['file1.py', 'file2.py']),
            (os.path.join(base_path, 'dir'), [], ['file3.py'])
        ]
        
        register_routes(app, base_path)
        
        expected_calls = [
            call(app, os.path.join(base_path, 'file1.py'), base_path.replace("/", os.sep)),
            call(app, os.path.join(base_path, 'file2.py'), base_path.replace("/", os.sep)),
            call(app, os.path.join(base_path, 'dir', 'file3.py'), base_path.replace("/", os.sep))
        ]
        
        mock_create_route_from_file.assert_has_calls(expected_calls, any_order=True)