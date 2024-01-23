from fastapi import FastAPI, HTTPException

from model_library.models import (
    ModelDeploymentTemplateCard,
    UserInformation,
    ModelDeploymentCard,
)
from model_library.library import ModelLibrary
from typing import Dict, Any
from model_library.utils import create_deployment_yaml

library = ModelLibrary()

# Create a FastAPI app
app = FastAPI()


# Get all endpoint
@app.get("/get_all")
def get_all() -> Dict[str, Any]:
    return library.to_dict()


@app.post("/create")
def create_kubernetes_deployment(
    template: ModelDeploymentTemplateCard, user: UserInformation
):
    card = ModelDeploymentCard(
        model_deployment_template=template, user_information=user
    )

    deployment = card.extract_values()

    kubernetes_deploytment = create_deployment_yaml(deployment.values, deployment.yaml)
    return kubernetes_deploytment


@app.post("/validate_template")
def validate_template(template: ModelDeploymentTemplateCard):
    return True


# Endpoint to check health
@app.get("/health/")
async def health():
    return HTTPException(status_code=200, detail="OK")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
