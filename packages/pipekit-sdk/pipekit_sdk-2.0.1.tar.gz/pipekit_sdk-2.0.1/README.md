[![Pipekit Logo](https://helm.pipekit.io/assets/pipekit-logo.png)](https://pipekit.io)

[Pipekit](https://pipekit.io) allows you to manage your workflows at scale. The control plane configures Argo Workflows for you in your infrastructure, enabling you to optimize multi-cluster workloads while reducing your cloud spend.  The team at Pipekit is also happy to support you through your Argo Workflows journey via commercial support.

# Pipekit Python SDK

## Installation

```bash
pip install pipekit-sdk
```

## Usage

```py
# The Pipekit SDK interacts with Hera Workflows classes
from hera.workflows import Container, Step, Steps, Workflow, script
from pipekit_sdk.service import PipekitService

# Create a Pipekit service that is used to talk to the Pipekit API
pipekit = PipekitService(token="<token>")

# List clusters and Pipes
clusters = pipekit.list_clusters()
pipes = pipekit.list_pipes()

@script()
def flip_coin() -> None:
    import random

    result = "heads" if random.randint(0, 1) == 0 else "tails"
    print(result)

# Create a Workflow using Hera
with Workflow(
    generate_name="coinflip-",
    annotations={
        "workflows.argoproj.io/description": (
            "This is an example of coin flip defined as a sequence of conditional steps."
        ),
    },
    entrypoint="coinflip",
    namespace="argo",
    service_account_name="argo",
) as w:
    heads = Container(
        name="heads",
        image="alpine:3.6",
        command=["sh", "-c"],
        args=['echo "it was heads"'],
    )
    tails = Container(
        name="tails",
        image="alpine:3.6",
        command=["sh", "-c"],
        args=['echo "it was tails"'],
    )

    with Steps(name="coinflip") as s:
        fc: Step = flip_coin()

        with s.parallel():
            heads(when=f"{fc.result} == heads")
            tails(when=f"{fc.result} == tails")

# Submit the Workflow to Pipekit
pipekit.submit(w, "<cluster-name>")

# Tail the logs
pipekit.print_logs(pipe_run.uuid)
```

## Further help
Please refer to the [Pipekit Documentation](https://docs.pipekit.io) for more information.
