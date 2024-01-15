import requests
from typing import Dict, Any


class FastAPIWrapper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_all(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/get_all")
        return response.json()

    def create_kubernetes_deployment(self, template: Dict, user: Dict) -> Any:
        data = {"template": template, "user": user}

        response = requests.post(f"{self.base_url}/create", json=data)
        print(response)
        return response.json()

    def validate_template(self, template: Dict) -> bool:
        response = requests.post(
            f"{self.base_url}/validate_template", json={"template": template}
        )
        return response.json()


if __name__ == "__main__":
    # Example usage
    api = FastAPIWrapper("http://0.0.0.0:8001")
    print(api.get_all())
    # print(api.create_kubernetes_deployment(template_data, user_data))
    # print(api.validate_template(template_data))
