import requests
import json


def deploy_generic_model(config_file_path):
    # Read the configuration from the file
    with open(config_file_path, "r") as file:
        config = file.read()

    # Prepare the request data
    data = {"config": config}

    # Define the URL and headers
    url = "http://0.0.0.0:8000/v1/deploy_generic_model"
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response
    if response.status_code == 200:
        print("Deployment successful.")
        print(response.json())
    else:
        print(f"Deployment failed with status code {response.status_code}.")
        print(response.text)


# Example usage
config_file = "llama_deploy.yaml"  # Replace with the path to your config file
deploy_generic_model(config_file)
