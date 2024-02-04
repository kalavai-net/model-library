# Model Library

This is a quick and burnable stand-alone API to retrieve, configure, and prepare for deploy model configs.

It covers seperate "Cards" that can be combined to create model templates. These cards are:

1. Architecture (Bad Name, read Framework) - The core technology used to serve the models (Llama.cpp, deepsparse, ray...)

2. Deployment - The machine hardware required to run the model

3. Model - The model related parameters, model ids, batch size etc

4. Model Deployment Template - A Model and Deployment pair, along with any benchmarks specific to this config

5. The Model Deployment - A Model Deployment Template complete with the required User information used to determine the namespace, API Keys etc.

This all comes together like so:

![Model Library](https://raw.githubusercontent.com/kalavai-net/model-library/main/data/model_library.png)



## API 

This is served through a simple API, which allows a disconnected way to:

1. Retrieve all of the Cards, from Architectures, up to Model Deployment Templates (One Click Deployments ptions)

2. Convert a Model Deployment Template + a User to a fullly instantiated kubernetes config, which can be deployed through Kube Watcher.

## UI

The current dirt quick UI is a streamlit endpoint that depends on both a Kube Watcher (on branch) and Model Library API

## TODO:

1. If this seems like a viable (but not long term approach) we can wrap this into its own docker file, and I guess prop it up as a service on a cluster?

2. We have the code in kubewatcher, we could quite possibly include a ray deployment option here too.


# Notes

## Kubernetes

1. When in doubt, kill a whole namespace

2. To connect to an endpoint with at Nodeport:
- Get your IP from .kube/config
- Get the Binded Port from kubectl get services -n namespace (which is in ~30000)
- This can be set in the config, but just dont.

3. You know when your deepsparse endpoint is running through pod logs
- kubectl get pods -n namespace
- kubectl logs <pod name> -n namespace