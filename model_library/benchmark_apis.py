import requests
import asyncio
import aiohttp
import pandas as pd
import time
from typing import List, Dict, Any
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio
from aiohttp import ClientTimeout

PROMPTS = [
    "\n\n### Instructions:\nWho was the first person to walk on the moon?\n\n### Response:\n",
    "\n\n### Instructions:\nWhat is the result of 457 multiplied by 123?\n\n### Response:\n",
    "\n\n### Instructions:\nTranslate 'Hello, how are you?' into Spanish.\n\n### Response:\n",
    "\n\n### Instructions:\nProvide a brief analysis of the theme of love in Shakespeare's 'Romeo and Juliet'.\n\n### Response:\n",
    "\n\n### Instructions:\nExplain the process of photosynthesis in plants.\n\n### Response:\n",
    "\n\n### Instructions:\nWhat is the significance of the cherry blossom festival in Japan?\n\n### Response:\n",
    "\n\n### Instructions:\nDescribe the basic principle behind blockchain technology.\n\n### Response:\n",
    "\n\n### Instructions:\nDiscuss Plato's Allegory of the Cave.\n\n### Response:\n",
    "\n\n### Instructions:\nWhat are the major rivers flowing through Brazil?\n\n### Response:\n",
    "\n\n### Instructions:\nDescribe the characteristics of Impressionist painting.\n\n### Response:\n",
    "\n\n### Instructions:\nWhat causes the Northern Lights?\n\n### Response:\n",
    "\n\n### Instructions:\nExplain Newton's three laws of motion.\n\n### Response:\n",
    "\n\n### Instructions:\nWhat are the ingredients of a traditional Margherita pizza?\n\n### Response:\n",
    "\n\n### Instructions:\nOutline the plot of 'The Great Gatsby' by F. Scott Fitzgerald.\n\n### Response:\n",
    "\n\n### Instructions:\nWhat is the Pythagorean Theorem?\n\n### Response:\n",
    "\n\n### Instructions:\nName the Seven Wonders of the Ancient World.\n\n### Response:\n",
    "\n\n### Instructions:\nHow does a computer perform basic arithmetic operations?\n\n### Response:\n",
    "\n\n### Instructions:\nWhat are the primary functions of the United Nations?\n\n### Response:\n",
    "\n\n### Instructions:\nDescribe the process of wine making.\n\n### Response:\n",
    "\n\n### Instructions:\nWhat are the different states of matter?\n\n### Response:\n",
    "\n\n### Instructions:\nFrom the following text, identify and list all the names of people mentioned: 'During the American Civil War, notable figures such as Abraham Lincoln, Robert E. Lee, Ulysses S. Grant, and Jefferson Davis played significant roles. Lincoln led the Union, while Davis was the President of the Confederacy. Generals Lee and Grant were prominent military leaders.'\n\n### Response:\n",
    "\n\n### Instructions:\nSummarize the following text: 'The Internet revolution has transformed the way we communicate, work, and obtain information. Originally created as a network for scientists to share data, it has evolved into a global information superhighway. Social media platforms, e-commerce, and online news have all become integral parts of daily life, fundamentally changing social dynamics and economies around the world.'\n\n### Response:\n",
    "\n\n### Instructions:\nIdentify the key points from this excerpt: 'Climate change is a significant challenge facing the planet. It's caused primarily by the increase of greenhouse gases like carbon dioxide in the atmosphere. The main contributors are fossil fuel burning and deforestation, leading to extreme weather events, rising sea levels, and changes in wildlife habitats.'\n\n### Response:\n",
    "\n\n### Instructions:\nAnalyze the main themes in this paragraph: 'In George Orwell's novel '1984', themes of totalitarianism, surveillance, and individuality are explored. The story depicts a society where the government, known as Big Brother, monitors and controls every aspect of people's lives, leading to a loss of freedom and personal identity.'\n\n### Response:\n",
    "\n\n### Instructions:\nFact-check the following statement and provide corrections if necessary: 'The Eiffel Tower was built in the 16th century as a military fortress. It's located in Berlin, Germany, and was used as a lookout post during World War II.'\n\n### Response:\n",
]

# Backend configurations
CONFIGS = {
    "LLAMACPP": {
        "url": "178.62.13.8",
        "port": 30767,
        "endpoint": "/v1/completions",
        "headers": {"accept": "application/json", "Content-Type": "application/json"},
        "format_payload": lambda prompt: {"prompt": prompt, "stop": ["\n", "###"]},
    },
    "DEEPSPARSE": {
        "url": "178.62.13.8",
        "port": 30091,
        "endpoint": "/v2/models/chat/infer",
        "headers": {},
        "format_payload": lambda prompt: {"prompt": prompt, "max_new_tokens": 100},
    },
}


# Function to perform serial requests
def perform_serial_requests(
    prompts: List[str], config_name: str, config_override: Dict = {}
) -> pd.DataFrame:
    config = CONFIGS[config_name]
    config.update(config_override)

    total_time = 0
    total_tokens = 0
    wall_time = time.time()

    success = 0
    for prompt in tqdm(prompts):
        try:
            formatted_payload = config["format_payload"](prompt)
            start_time = time.time()
            url = f"http://{config['url']}:{config['port']}{config['endpoint']}"
            response = requests.post(
                url, headers=config["headers"], json=formatted_payload
            )
            end_time = time.time()
            data = response.json()

            total_time += end_time - start_time
            total_tokens += data["usage"]["total_tokens"]
            success += 1

        except Exception as e:
            print(f"Call to benchmark prompt failed: {e}")

    average_time = total_time / success
    average_tokens = total_tokens / success

    wall_time = time.time() - wall_time
    tps = total_tokens / wall_time

    return pd.DataFrame(
        [
            {
                "type": "serial",
                "average_response_time": average_time,
                "average_tokens_returned": average_tokens,
                "total_tokens_returned": total_tokens,
                "wall_time": wall_time,
                "tps": tps,
            }
        ]
    )


# Async request function
async def perform_async_request(
    session, prompt: str, config_name: str, config_override: Dict = {}
) -> Dict[str, Any]:
    config = CONFIGS[config_name]
    config.update(config_override)
    formatted_payload = config["format_payload"](prompt)
    start_time = time.time()

    timeout = ClientTimeout(total=600)

    url = f"http://{config['url']}:{config['port']}{config['endpoint']}"

    async with session.post(
        url, json=formatted_payload, headers=config["headers"], timeout=timeout
    ) as response:
        try:
            data = await response.json()
        except:
            print(response)
        end_time = time.time()
        return {
            "model_id": data["model"],
            "response_time": end_time - start_time,
            "tokens_returned": data["usage"]["total_tokens"],
        }


# Function to perform asynchronous requests


async def perform_async_requests(
    prompts: List[str], config_name: str, config_override: Dict = {}
) -> pd.DataFrame:
    config = CONFIGS[config_name]
    config.update(config_override)
    wall_time = time.time()
    async with aiohttp.ClientSession(headers=config["headers"]) as session:
        tasks = [
            perform_async_request(session, prompt, config_name) for prompt in prompts
        ]

        results = []
        for f in tqdm_asyncio.as_completed(tasks):
            result = await f
            results.append(result)

    total_time = sum(result["response_time"] for result in results)
    total_tokens = sum(result["tokens_returned"] for result in results)
    wall_time = time.time() - wall_time
    tps = total_tokens / wall_time

    average_time = total_time / len(prompts)
    average_tokens = total_tokens / len(prompts)

    return pd.DataFrame(
        [
            {
                "type": "async",
                "average_response_time": average_time,
                "average_tokens_returned": average_tokens,
                "total_tokens_returned": total_tokens,
                "wall_time": wall_time,
                "tps": tps,
            }
        ]
    )


def benchmark_model(
    backend: str, port=None, endpoint=None, url=None, test_prompts=None, do_async=False
):
    # Here, add your list of test_prompts

    if test_prompts is None:
        test_prompts = PROMPTS

    config_override = {}
    if port:
        config_override["port"] = port
    if endpoint:
        config_override["endpoint"] = endpoint
    if url:
        config_override["url"] = url

    if backend in CONFIGS:
        serial_results = perform_serial_requests(
            test_prompts, backend, config_override=config_override
        )
        if do_async:
            loop = asyncio.get_event_loop()
            async_results = loop.run_until_complete(
                perform_async_requests(
                    test_prompts, backend, config_override=config_override
                )
            )
            combined_results = pd.concat([serial_results, async_results])
        else:
            combined_results = serial_results

        print(combined_results)
    else:
        print(f"Unsupported backend: {backend}")

    return combined_results


import time
import logging
from model_library.benchmark_apis import benchmark_model
from tqdm import tqdm
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class KubernetesBenchmark:
    def __init__(
        self,
        deployment_template: Any,
        deploy: bool = True,
        undeploy: bool = True,
        public_url: str = "178.62.13.8",
        live_service_cutout: int = 10 * 60,
        user: Optional[Any] = None,
    ):
        """
        Initialize the KubernetesBenchmark class.

        :param deployment_template: The deployment template object.
        :param public_url: Public URL for the deployment.
        :param live_service_cutout: Timeout for the service to become live.
        :param user: User information object.
        :param deploy: Flag to deploy before testing.
        :param undeploy: Flag to delete deployment after testing.
        """
        self.deployment_template = deployment_template
        self.public_url = public_url
        self.live_service_cutout = live_service_cutout
        self.user = user or UserInformation(
            id="benchmark", namespace="benchmark", API_key=""
        )
        self.deployment_name = deployment_template.params["deployment_name"]
        self.port = None
        self.backend_to_test = "LLAMACPP"  # TODO: Make this configurable if needed
        self.undeploy = undeploy
        self.deploy_first = deploy
        self.architecture = self.deployment_template.model_card.architecture

    def deploy(self) -> None:
        """
        Deploy the model.
        """
        if not self.deploy_first:
            if not self.architecture.check_health(port=self.port, url=self.public_url):
                raise Exception("Cannot test an unavailable model.")

        else:
            delete_deployment(self.user.namespace, self.deployment_name)

        logging.info("Deploying the model.")
        deployment = ModelDeploymentCard(
            user_information=self.user,
            model_deployment_template=self.deployment_template,
        )
        config = deployment.extract_deployment_config()
        deploy_generic_model(config)

        time.sleep(5)  # Wait for the deployment to initialize
        logging.info("Model deployed.")

    def wait_for_service(self) -> int:
        """
        Wait for the service to become live.

        :return: The time waited for the service to become live.
        """
        logging.info("Waiting for the live service.")
        deployments = list_deployments(namespace=self.user.namespace)
        deployment = deployments[self.deployment_name]
        self.port = max(deployment["ports"][0])

        warmup_time = 0
        interval = 10

        with tqdm(total=self.live_service_cutout) as pbar:
            while warmup_time < self.live_service_cutout:
                if self.architecture.check_health(port=self.port, url=self.public_url):
                    break
                time.sleep(interval)
                warmup_time += interval
                pbar.update(interval)

        logging.info(f"Service is live. Warmup time: {warmup_time} seconds.")
        return warmup_time

    def run_benchmark(self) -> Dict[str, Any]:
        """
        Run the benchmark.

        :return: Dictionary of benchmark results.
        """
        logging.info("Running benchmarks.")
        benchmarks = benchmark_model(
            self.backend_to_test, port=self.port, url=self.public_url
        )
        return benchmarks.to_dict("records")

    def cleanup(self) -> None:
        """
        Clean up after benchmarking.
        """
        logging.info("Cleaning up the deployment.")
        if self.undeploy:
            delete_deployment(self.user.namespace, self.deployment_name)

    def benchmark_deployment(self) -> Dict[str, Any]:
        """
        Perform the entire benchmarking process.

        :return: A dictionary containing benchmarking results and metadata.
        """
        self.deploy()
        warmup_time = self.wait_for_service()

        if warmup_time >= self.live_service_cutout:
            logging.warning("Service did not become live within the cutoff time.")
            self.cleanup()

            return {
                "benchmarks": {},
                "warmup_time": warmup_time,
                "template": self.deployment_template,
                "error": "Cut off start time limit reached.",
            }

        try:
            benchmarks = self.run_benchmark()
        except Exception as e:
            return {
                "benchmarks": {},
                "warmup_time": warmup_time,
                "template": self.deployment_template,
                "error": f"Failed to benchmark. {e}",
            }

        return {
            "benchmarks": benchmarks,
            "warmup_time": warmup_time,
            "template": self.deployment_template,
            "deployment": self.deployment_name,
        }


if __name__ == "__main__":
    backend_to_test = "LLAMACPP"
    port = 30767
    num_prompts = 2
    benchmark_model(backend_to_test, port=port)
