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

OPEN_TOOL_LIBRARY_DEPLOYMENT_CARD = ModelDeploymentTemplateCard(
    id=str(uuid.uuid4()),
    name="The Open Magic Toolbox",
    description="The Magic Toolbox for Infinate Tool Use Agents",
    model_card=TOOL_LIBRARY,
    deployment_card=TOOL_LIBRARY_DEPLOYMENT,
    viable_deployment_cards=[TOOL_LIBRARY_DEPLOYMENT, TOOL_LIBRARY_DEPLOYMENT_AUTH],
    benchmarks=[],
    params={"deployment_name": "tool-library-unauthenticated"},
)

TOOL_LIBRARY_DEPLOYMENT_CARD = ModelDeploymentTemplateCard(
    id=str(uuid.uuid4()),
    name="The Closed Magic Toolbox",
    description="The Magic Toolbox for Infinate Tool Use Agents, with authentification",
    model_card=TOOL_LIBRARY,
    deployment_card=TOOL_LIBRARY_DEPLOYMENT_AUTH,
    viable_deployment_cards=[TOOL_LIBRARY_DEPLOYMENT, TOOL_LIBRARY_DEPLOYMENT_AUTH],
    benchmarks=[],
    params={"deployment_name": "tool-library-authenticated"},
)

LOCAL_AI_DEPLOYMENT_TEMPLATE_CARD = ModelDeploymentTemplateCard(
    id=str(uuid.uuid4()),
    name="Local AI CPU Deployment",
    description="Deploying Local AI on CPU",
    model_card=LOCAL_AI_MODEL_CARD,
    deployment_card=LOCAL_AI_DEPLOYMENT_CARD,
    params={"deployment_name": "local-ai-cpu"}
)

RAG_DEPLOYMENT_TEMPLATE_CARD = ModelDeploymentTemplateCard(
    id="rag-tool",
    name="RAG Tool Deployment",
    description="Deployment template for RAG tool with Python 3.8-slim container.",
    model_card=RAG_MODEL_CARD,
    deployment_card=RAG_DEPLOYMENT_CARD,
    params={        
        "deployment_name": "rag-tool-test",
        "rag_use_auth": "False",
        "rag_master_key": ""
    }
)

def curate_cards():
    architecture_cards = []
    for name, obj in globals().items():
        if isinstance(obj, ModelDeploymentTemplateCard):
            architecture_cards.append(obj)
    return architecture_cards


MODEL_DEPLOYMENT_TEMPLATES = curate_cards()
