import streamlit as st

st.title("One Click Deployments")

if "config" not in st.session_state:
    st.session_state["config"] = None

if "deployments" not in st.session_state:
    st.session_state["deployments"] = None


# Get a list of all the models
def deploy_generic_model(config):
    import requests
    import json

    # Prepare the request data
    data = {"config": config}

    # Define the URL and headers
    url = "http://0.0.0.0:8000/v1/deploy_generic_model"
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response
    if response.status_code == 200:
        st.write(response)
        print("Deployment successful.")
        return response.json()
    else:
        print(f"Deployment failed with status code {response.status_code}.")
        st.write(response.text)
        return None


def list_deployments(namespace):
    import requests
    import json

    # Prepare the request data
    data = {"namespace": namespace}

    # Define the URL and headers
    url = "http://0.0.0.0:8000/v1/list_deepsparse_deployments"
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response
    if response.status_code == 200:
        print("Request successful.")
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}.")
        return None


def get_deployments(config):
    import requests
    import json

    # Prepare the request data
    data = {"config": config}

    # Define the URL and headers
    url = "http://0.0.0.0:8000/v1/deploy_generic_model"
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response
    if response.status_code == 200:
        st.write(response)
        print("Deployment successful.")
        return response.json()
    else:
        print(f"Deployment failed with status code {response.status_code}.")
        st.write(response.text)
        return None


def delete_deployment(namespace, deployment_name):
    import requests
    import json

    # Prepare the request data
    data = {"namespace": namespace, "deployment_name": deployment_name}

    # Define the URL and headers
    url = "http://0.0.0.0:8000/v1/delete_deepsparse_model"
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response
    if response.status_code == 200:
        print("Delete request successful.")
        return response.json()
    else:
        print(f"Delete request failed with status code {response.status_code}.")
        return None


from model_library.api_wrapper import FastAPIWrapper
from model_library.models import *

library = FastAPIWrapper("http://0.0.0.0:8001")

with st.sidebar:
    st.header("User")
    namespace = st.text_input("User Name", "adam")
    api_key = st.text_input("API Key", "XXXXXXX")

    user = UserInformation(id=namespace, namespace=namespace, API_key=api_key)

templates = {
    f'{t["id"]} {t["name"]}': t
    for t in library.get_all()["ModelDeploymentTemplateCard"]
}

template_id = st.selectbox("Template", templates.keys())

template = templates[template_id]

st.header(template["name"])
st.info(template["description"])

with st.expander("Model Card"):
    st.write(template["model_card"])

with st.expander("Architecture Card"):
    st.write(template["model_card"]["architecture"])

with st.expander("Deployment"):
    st.write(template["deployment_card"])

if st.button("Generate Config"):
    config = library.create_kubernetes_deployment(template=template, user=user.dict())
    st.session_state["config"] = config

    with st.expander("Config"):
        st.write(config)

if st.session_state.config:
    if st.button("Deploy"):
        res = deploy_generic_model(config=st.session_state.config)
        print(res)


ctitle, crefresh = st.columns(2)
with ctitle:
    st.header("Deployments")
with crefresh:
    if st.button("Refresh"):
        st.session_state.deployments = list_deployments(user.namespace)

if st.session_state.deployments:
    for id, data in st.session_state.deployments.items():
        a, b = st.columns(2)
        with a:
            with st.expander(id):
                st.write(data)

        with b:
            if st.button("Delete", key=id):
                res = delete_deployment(user.namespace, id)
                if res:
                    st.success("Deployment Deleted")
                else:
                    st.error("Failed to Delete")
