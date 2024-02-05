from model_library.models import ArchitectureCard
import uuid

LLAMA_CPP = ArchitectureCard(
    name="Llama.cpp (python)",
    id=str(uuid.uuid4()),
    description="The python llama.cpp engine",
    tags={"cpu": True, "gpu": True},
    deployment_yaml="llama_cpp_python.yaml",
    health_endpoint="v1/models",
)

DEEPSPARSE = ArchitectureCard(
    id=str(uuid.uuid4()),
    deployment_yaml="deepsparse_deployment.yaml",
    name="deepsparse",
    description="Deepsparse Deployment for Chat Model",
    tags={"type": "deepsparse", "version": "v1.6.1"},
)


TOOL_LIBRARY = ArchitectureCard(
    name="tool-library",
    id=str(uuid.uuid4()),
    description="The Magic Toolbox",
    tags={},
    deployment_yaml="tool_library_deployment.yaml",
    health_endpoint="health",
)


# At the bottom of architectures.py
def curate_architecture_cards():
    architecture_cards = []
    for name, obj in globals().items():
        if isinstance(obj, ArchitectureCard):
            architecture_cards.append(obj)
    return architecture_cards


# Curate the list of ArchitectureCard instances
# Example Instances
LOCAL_AI_ARCHITECTURE = ArchitectureCard(
    id=str(uuid.uuid4()),
    deployment_yaml="local_ai_cpu.yaml",
    name="Local AI CPU Deployment",
    description="Local AI deployment with CPU support",
    tags={"cpu": True, "gpu": False}
)

KALAVAI_RAG_ARCHITECTURE = ArchitectureCard(
    id=str(uuid.uuid4()),
    deployment_yaml="kalavai_rag_deployment.yaml",
    name="Kalavai Rag Tool",
    description="RAG tool deployment architecture.",
    tags={},
    health_endpoint="/health"  # or specify if applicable
)

ARCHITECTURES = curate_architecture_cards()
