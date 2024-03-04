import requests
from typing import Dict, Any


class ModelLibraryClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers['X-API-KEY'] = self.api_key


    def get_all(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/get_all", headers=self.headers)
        return response.json()

    def create_kubernetes_deployment(self, template: Dict, user: Dict) -> Any:
        data = {"template": template, "user": user}

        response = requests.post(f"{self.base_url}/create", json=data, headers=self.headers)
        print(response)
        return response.json()

    def validate_template(self, template: Dict) -> bool:
        response = requests.post(
            f"{self.base_url}/validate_template", json={"template": template}, headers=self.headers
        )
        return response.json()

    def health(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/health", headers=self.headers)
        except:
            return False
        return response.status_code == 200

if __name__ == "__main__":
    # Example usage
    api = ModelLibraryClient("http://0.0.0.0:8001")
    print(api.get_all())
    # print(api.create_kubernetes_deployment(template_data, user_data))
    # print(api.validate_template(template_data))
