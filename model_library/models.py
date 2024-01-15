from pydantic import BaseModel, HttpUrl, Field
from typing import List, Tuple, Dict, Optional, Any
import uuid

# Updated Pydantic models with added `id` and `API_key` for UserInformation


class ArchitectureCard(BaseModel):
    id: str
    deployment_yaml: str
    name: str
    description: str
    tags: Dict[str, Any]


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

    def extract_values(self) -> Dict[str, Any]:
        values = {}
        values.update(self.user_information.model_dump())
        values.update(self.model_deployment_template.model_card.params)
        values.update(self.model_deployment_template.deployment_card.params)
        values.update(self.model_deployment_template.params)

        return DeploymentParams(
            values=values,
            yaml=self.model_deployment_template.model_card.architecture.deployment_yaml,
        )
