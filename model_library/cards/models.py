from model_library.models import ModelCard
from model_library.cards.architectures import *

LLAMA_CPP_LLAMA_2_7b_CHAT_Q2_GGUF = ModelCard(
    id="3",
    architecture=LLAMA_CPP,
    params={
        "model_path": "/model/llama-2-7b-chat.Q2_K.gguf",
        "hf_repo_id": "TheBloke/Llama-2-7B-Chat-GGUF",
        "hf_filename": "llama-2-7b-chat.Q2_K.gguf",
        "volume_name": "awesome-model-storage",
        "pvc_name": "awesome-model-pvc",
    },
)

DEEPSPARSE_CHAT = ModelCard(
    id=str(uuid.uuid4()),
    architecture=DEEPSPARSE,
    params={
        "image": "ghcr.io/neuralmagic/deepsparse:v1.6.1",
        "sparsezoo_models_path": "/home/user/llama",
        "container_port": 5543,
        "task": "chat",
        "model_path": "zoo:llama2-7b-llama2_chat_llama2_pretrain-base_quantized",
        "batch_size": 1,
        "num_workers": 4,
        "num_cores": 4,
    },
)


def curate_model_cards():
    architecture_cards = []
    for name, obj in globals().items():
        if isinstance(obj, ModelCard):
            architecture_cards.append(obj)
    return architecture_cards


# Curate the list of ArchitectureCard instances

MODELS = curate_model_cards()
