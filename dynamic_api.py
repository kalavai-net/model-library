import requests
from typing import Any
import asyncio


class DynamicAPIWrapper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.schema_url = f"{self.base_url}/openapi.json"
        self.methods = {}
        self._fetch_and_create_methods()

    def _fetch_and_create_methods(self):
        schema = requests.get(self.schema_url).json()
        paths = schema["paths"]
        for path, methods in paths.items():
            for method_type, details in methods.items():
                method_name = details["operationId"]
                self._create_method(method_name, path, method_type)

    def _create_method(self, method_name: str, path: str, method_type: str):
        url = self.base_url + path

        async def method(**kwargs) -> Any:
            if method_type == "get":
                response = requests.get(url, params=kwargs)
            elif method_type == "post":
                response = requests.post(url, json=kwargs)
            else:
                raise NotImplementedError(f"Method {method_type} not implemented.")
            return response.json()

        setattr(self, method_name, method)
        self.methods[method_name] = method

    def list_methods(self) -> list:
        """Returns a list of all dynamically generated methods."""
        return list(self.methods.keys())

    def __getattr__(self, name):
        if name in self.methods:
            return self.methods[name]
        raise AttributeError(f"No such method: {name}")


# Usage
base_url = "http://178.62.13.8:30091"
api_wrapper = DynamicAPIWrapper(base_url)

# List all available methods
methods = api_wrapper.list_methods()
print("Available methods:", methods)

# You can also call any of these methods, for example:
# response = asyncio.run(api_wrapper.some_method_name())
