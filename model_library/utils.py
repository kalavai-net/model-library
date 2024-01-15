from string import Template
import pkg_resources
from typing import Optional
import os


# At the bottom of architectures.py
def curate_objects(pydantic_class):
    architecture_cards = []
    for name, obj in globals().items():
        if isinstance(obj, pydantic_class):
            architecture_cards.append(obj)
    return architecture_cards


def create_deployment_yaml(values, template_file):
    """
    generates a yaml deployment for generic_serving
    """

    template = Template(load_from_pkg_resources(template_file))
    result = template.substitute(values)

    return result


def load_from_pkg_resources(
    relative_path: str, package_name: str = "model_library"
) -> Optional[str]:
    # relative_path += "kubernetes_configs/" + relative_path

    relative_path = os.path.join("kubernetes_configs", relative_path)
    try:
        # Check if the resource exists and then read it
        if pkg_resources.resource_exists(package_name, relative_path):
            return pkg_resources.resource_string(package_name, relative_path).decode(
                "utf-8"
            )
    except Exception as e:
        print(f"Failed to load from package resources: {e}")
    return None


if __name__ == "__main__":
    # Example usage
    content = load_from_pkg_resources("deployments.yaml")

    if content is not None:
        print("Content loaded:", content)
    else:
        print("Content could not be loaded.")

    yaml = create_deployment_yaml({"namespace": "adam"}, "deployments.yaml")

    print(yaml)
