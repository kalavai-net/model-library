from pydantic import BaseModel
from typing import Type, Dict, List, Any

from model_library.models import (
    ArchitectureCard,
    ModelCard,
    DeploymentCard,
    ModelDeploymentTemplateCard,
)
from model_library import ARCHITECTURES, MODELS, MODEL_DEPLOYMENT_TEMPLATES, DEPLOYMENTS


class ModelLibrary:
    def __init__(
        self,
        model_types: List[Type[BaseModel]] = [
            ArchitectureCard,
            ModelCard,
            DeploymentCard,
            ModelDeploymentTemplateCard,
        ],
    ):
        self.model_types = model_types
        self.models = {model_type: [] for model_type in model_types}
        self.auto_register()

        for a in ARCHITECTURES + MODEL_DEPLOYMENT_TEMPLATES + MODELS + DEPLOYMENTS:
            self.register(a)

    def register(self, model_instance: BaseModel):
        for model_type in self.model_types:
            if isinstance(model_instance, model_type):
                self.models[model_type].append(model_instance)

    def to_dict(self) -> Dict[str, List[Any]]:
        return {
            model_type.__name__: [model.model_dump() for model in instances]
            for model_type, instances in self.models.items()
        }

    def get_models(self):
        return self.models

    def auto_register(self):
        # Check both local and global scope
        for scope in [locals(), globals()]:
            for obj in scope.values():
                if isinstance(obj, BaseModel) and type(obj) in self.model_types:
                    self.register(obj)


if __name__ == "__main__":
    from model_library.cards.architectures import *

    model_library = ModelLibrary(
        [
            ArchitectureCard,
            ModelCard,
            DeploymentCard,
            ModelDeploymentTemplateCard,
        ]
    )

    # Convert to dictionary
    print(model_library.to_dict())
