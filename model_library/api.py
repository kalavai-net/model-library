import os

from fastapi import FastAPI, HTTPException, Depends
from starlette.requests import Request


from model_library.models import (
    ModelDeploymentTemplateCard,
    UserInformation,
    ModelDeploymentCard,
)
from model_library.library import ModelLibrary
from typing import Dict, Any
from model_library.utils import create_deployment_yaml

library = ModelLibrary()



# Configuration handling
# Conservatively assume Auth is enabled if anything other than these false values are set.
USE_AUTH = not os.getenv("ML_USE_AUTH", "True").lower() in ("false", "0", "f", "no")
MASTER_KEY = os.getenv("ML_MASTER_KEY")

if USE_AUTH:
    assert MASTER_KEY is not None, "If you are using auth, you must set a master key using the 'ML_MASTER_KEY' environment variable."
else:
    logger.warning("Warning: Authentication is disabled. This should only be used for testing.")


# Create a FastAPI app
app = FastAPI()

# API Key Validation
async def verify_api_key(request: Request):
    if not USE_AUTH:
        return
    api_key = request.headers.get("X-API-KEY")
    if api_key != MASTER_KEY:
        print(api_key, MASTER_KEY)
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

# Get all endpoint
@app.get("/get_all")
def get_all(api_key: str = Depends(verify_api_key)) -> Dict[str, Any]:
    return library.to_dict()


@app.post("/create")
def create_kubernetes_deployment(
    template: ModelDeploymentTemplateCard, user: UserInformation, 
    api_key: str = Depends(verify_api_key)
):
    card = ModelDeploymentCard(
        model_deployment_template=template, user_information=user
    )

    deployment = card.extract_values()

    kubernetes_deploytment = create_deployment_yaml(deployment.values, deployment.yaml)
    return kubernetes_deploytment


@app.post("/validate_template")
def validate_template(
    template: ModelDeploymentTemplateCard,
    api_key: str = Depends(verify_api_key)
    ):
    return True


# Endpoint to check health
@app.get("/health")
async def health():
    return HTTPException(status_code=200, detail="OK")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
