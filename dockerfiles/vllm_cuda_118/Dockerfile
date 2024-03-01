FROM nvidia/cuda:11.8.0-devel-ubuntu22.04 AS dev

RUN apt-get update -y \
    && apt-get install -y python3-pip

WORKDIR /workspace

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install vllm==0.2.6

ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server", "--model", "TheBloke/TinyLlama-1.1B-Chat-v0.3-AWQ", "--quantization", "awq", "--chat-template", "./examples/template_chatml.jinja"]