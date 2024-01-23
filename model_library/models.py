from pydantic import BaseModel, HttpUrl, Field
from typing import List, Tuple, Dict, Optional, Any
from model_library.utils import create_deployment_yaml
import uuid
import requests

# Updated Pydantic models with added `id` and `API_key` for UserInformation


class ArchitectureCard(BaseModel):
    id: str
    deployment_yaml: str
    name: str
    description: str
    tags: Dict[str, Any]

    health_endpoint: str = None

    def check_health(self, url, port):
        if self.health_endpoint is None:
            return False

        full_url = f"http://{url}:{port}/{self.health_endpoint}"
        try:
            response = requests.get(full_url)
            return response.status_code == 200
        except:
            return False


class ModelCard(BaseModel):
    id: str
    architecture: ArchitectureCard
    params: Dict[str, Any]


class DeploymentCard(BaseModel):
    id: str
    params: Dict[str, Any]


class Benchmark(BaseModel):
    id: str
    description: str
    results: Dict[str, Any]


class ModelDeploymentTemplateCard(BaseModel):
    id: str
    name: str
    description: str
    model_card: ModelCard
    benchmarks: Optional[List[Benchmark]] = None
    deployment_card: DeploymentCard
    viable_deployment_cards: List[DeploymentCard] = []
    params: Dict[str, Any]


class UserInformation(BaseModel):
    id: str
    namespace: str
    API_key: str


class DeploymentParams(BaseModel):
    values: Dict[str, Any]
    yaml: str


class ModelDeploymentCard(BaseModel):
    model_deployment_template: ModelDeploymentTemplateCard
    user_information: UserInformation
    override_params: Dict[str, Any] = {}

    def extract_values(self) -> Dict[str, Any]:
        values = {}
        values.update(self.user_information.model_dump())
        values.update(self.model_deployment_template.model_card.params)
        values.update(self.model_deployment_template.deployment_card.params)
        values.update(self.model_deployment_template.params)
        values.update(self.override_params)

        return DeploymentParams(
            values=values,
            yaml=self.model_deployment_template.model_card.architecture.deployment_yaml,
        )

    def extract_deployment_config(self) -> str:
        values = self.extract_values()
        config = create_deployment_yaml(values=values.values, template_file=values.yaml)
        return config
