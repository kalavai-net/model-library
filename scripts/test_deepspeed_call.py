"""
Inference calls to a DeepSparse deployment

E.G. docker deployment

"""
import time
import requests

SERVICE_URL = "http://178.62.13.8"
SERVICE_PORT = "30091"
SERVICE_ENDPOINT = "/v2/models/chat/infer"

url = f"{SERVICE_URL}:{SERVICE_PORT}{SERVICE_ENDPOINT}"  # Server's port default to 5543
prompt = """
\n\n### Instructions:\nIf I'm a vegetarian, what can I eat?\n\n### Response:\n
"""
obj = {"prompt": prompt, "max_new_tokens": 100}

t = time.time()
response = requests.post(url, json=obj)
print(response.text)

total_time = time.time() - t
per_token_time = total_time / len(response.text.split())
print(f"{total_time:.2f}s, ({per_token_time:.2f}s per token)")
