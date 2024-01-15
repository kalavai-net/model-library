from model_library.models import ArchitectureCard
import uuid

LLAMA_CPP = ArchitectureCard(
    name="Llama.cpp (python)",
    id=str(uuid.uuid4()),
    description="The python llama.cpp engine",
    tags={"cpu": True, "gpu": True},
    deployment_yaml="llama_cpp_python.yaml",
)

DEEPSPARSE = ArchitectureCard(
    id=str(uuid.uuid4()),
    deployment_yaml="deepsparse_deployment.yaml",
    name="deepsparse",
    description="Deepsparse Deployment for Chat Model",
    tags={"type": "deepsparse", "version": "v1.6.1"},
)


# At the bottom of architectures.py
def curate_architecture_cards():
    architecture_cards = []
    for name, obj in globals().items():
        if isinstance(obj, ArchitectureCard):
            architecture_cards.append(obj)
    return architecture_cards


# Curate the list of ArchitectureCard instances

ARCHITECTURES = curate_architecture_cards()
