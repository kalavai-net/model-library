import uuid
from model_library.models import DeploymentCard


MINIMAL_CPU_DEPLOYMENT = DeploymentCard(
    id="4",
    description="Minimal Deployment for llama.cpp",
    params={
        "replicas": 1,
        "num_cpus": 4,
        "ram_memory": "12Gi",
        "pvc_storage_request": "24Gi",
    },
)

MEDIUM_CPU_DEPLOYMENT = DeploymentCard(
    id="4",
    description="Medium CPU Deployment for llama.cpp",
    params={
        "replicas": 2,
        "num_cpus": 8,
        "ram_memory": "24Gi",
        "pvc_storage_request": "24Gi",
    },
)


DEEPSPARSE_MINIMAL = DeploymentCard(
    id=str(uuid.uuid4()),
    params={
        "replicas": 1,
        "cpu_limits": "6",
        "memory_limits": "18Gi",
        "cpu_requests": "6",
        "memory_requests": "18Gi",
        "volume_mount_name": "deepsparse-model-storage",
        "mount_path": "/home/user",
        "volume_name": "deepsparse-model-storage",
        "pvc_name": "deepsparse-model-pvc",
        "service_name": "deepsparse-model",
        "port_name": "https",
        "port": 5543,
        "pvc_storage_request": "30Gi",
    },
)

TOOL_LIBRARY_DEPLOYMENT = DeploymentCard(
    id="tool_library_deployment",
    params={
        "use_auth": "False",
    },
)

TOOL_LIBRARY_DEPLOYMENT_AUTH = DeploymentCard(
    id="tool_library_deployment",
    params={
        "use_auth": "True",
    },
)


def curate_deployment_cards():
    architecture_cards = []
    for name, obj in globals().items():
        if isinstance(obj, DeploymentCard):
            architecture_cards.append(obj)
    return architecture_cards

LOCAL_AI_DEPLOYMENT_CARD = DeploymentCard(
    id=str(uuid.uuid4()),
    params={
        "cpu_limits": "2",
        "memory_limits": "10Gi",
        "cpu_requests": "2",
        "memory_requests": "10Gi"
    }
)

# Deployment Specific Details
RAG_DEPLOYMENT_CARD = DeploymentCard(
    id=str(uuid.uuid4()),
    params={
        "cpu_limits": "2",
        "memory_limits": "4Gi",
        "cpu_requests": "2",
        "memory_requests": "4Gi",
        "replicas": 1,
    }
)

# Curate the list of ArchitectureCard instances

DEPLOYMENTS = curate_deployment_cards()
