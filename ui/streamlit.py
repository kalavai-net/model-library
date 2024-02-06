import streamlit as st

st.title("One Click Deployments")

if "config" not in st.session_state:
    st.session_state["config"] = None

if "deployments" not in st.session_state:
    st.session_state["deployments"] = None

from model_library.client import ModelLibraryClient
from kube_watcher.client import KubeWatcherClient
from model_library.models import *


with st.sidebar:
    st.header("User")
    namespace = st.text_input("User Name", "adam")
    api_key = st.text_input("API Key", "XXXXXXX")
    user = UserInformation(id=namespace, namespace=namespace, API_key=api_key)

    st.header("Model Library")
    model_library_url = st.text_input("Model Library URL", "http://0.0.0.0:8001")
    model_library_api_key = st.text_input("API Key", "XXXX")

    library = ModelLibraryClient(model_library_url, model_library_api_key)

    if library.health():
        st.success("Model Library is healthy")
    else:
        st.error("Model Library is not available")

    st.session_state["library"] = library

    st.header("Kube Watcher")
    kube_watcher_url = st.text_input("Kube Watcher URL", "http://0.0.0.0:8000")
    kube_watcher_api_key = st.text_input("API Key", "")
    kube_watcher = KubeWatcherClient(kube_watcher_url, kube_watcher_api_key)

    

    if kube_watcher.health():
        st.success("Kube Watcher is healthy")

    else:
        st.error("Kube Watcher is not available")

    st.session_state["kube_watcher"] = kube_watcher 

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

with st.expander("Deployment Template Card"):
    st.write(template)

if st.button("Generate Config"):
    config = library.create_kubernetes_deployment(template=template, user=user.dict())
    st.session_state["config"] = config

    with st.expander("Config"):
        st.write(config)

if st.session_state.config:
    if st.button("Deploy"):
        res = kube_watcher.deploy_generic_model({"config":st.session_state.config})
        print(res)


ctitle, crefresh = st.columns(2)
with ctitle:
    st.header("Deployments")
with crefresh:
    if st.button("Refresh"):
        st.session_state.deployments = kube_watcher.get_resources_with_label(user.namespace, label_key="app")

if st.session_state.deployments:
    for data in st.session_state.deployments:
        a, b, c,d, e  = st.columns(5)
        with a:
            st.write(data["name"])
        with b:
            st.write(data["label_key"])
        with c:
            st.write(data["label_value"])
        with d:
            if len(data["node_ports"]):

                port = max(data["node_ports"])
                url = f"http://178.62.13.8:{port}/"
                st.write(f"[{port}]({url})")

        with e:
            if st.button("Delete", key=data["name"]):
                res = kube_watcher.delete_labeled_resources({"namespace":user.namespace, "label":data["label_key"], "value":data["label_value"]})

                if res:
                    st.success("Deployment Deleted")
                    st.write(res)
                else:
                    st.error("Failed to Delete")
        
        with st.expander(data["name"]):
            st.write(data)

        
