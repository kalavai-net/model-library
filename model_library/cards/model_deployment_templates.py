from model_library.cards.deployments import *
from model_library.cards.models import *

from model_library.models import ModelDeploymentTemplateCard

MINIMAL_LLAMACPP_DEPLOYMENT = ModelDeploymentTemplateCard(
    id="1",
    name="Llama 2 7B Minimal",
    description="A minimal Llama 2 7B inference deployment based on Llama.cpp python, running on a CPU",
    model_card=LLAMA_CPP_LLAMA_2_7b_CHAT_Q2_GGUF,
    deployment_card=MINIMAL_CPU_DEPLOYMENT,
    viable_deployment_cards=[MINIMAL_CPU_DEPLOYMENT, MEDIUM_CPU_DEPLOYMENT],
    benchmarks=[],
    params={"deployment_name": "llama-cpp-llama2-7b"},
)


MINIMAL_DEEPSPEED_DEPLOYMENT = ModelDeploymentTemplateCard(
    id=str(uuid.uuid4()),
    name="Deepsparse Chat",
    description="A minimal Llama 7B inference deployment based on DeepSparse python, running on a CPU",
    model_card=DEEPSPARSE_CHAT,
    deployment_card=DEEPSPARSE_MINIMAL,
    viable_deployment_cards=[DEEPSPARSE_MINIMAL],
    benchmarks=[],
    params={"deployment_name": "deepspeed-llama2-7b"},
)


def curate_cards():
    architecture_cards = []
    for name, obj in globals().items():
        if isinstance(obj, ModelDeploymentTemplateCard):
            architecture_cards.append(obj)
    return architecture_cards


MODEL_DEPLOYMENT_TEMPLATES = curate_cards()
