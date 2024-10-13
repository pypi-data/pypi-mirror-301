# mypy: disable-error-code="call-arg"
import logging

import msgspec
from kubernetes import client

from lueur.make_id import make_id
from lueur.models import K8SMeta, Resource
from lueur.platform.k8s.client import AsyncClient, Client

__all__ = ["explore_pod"]
logger = logging.getLogger("lueur.lib")


async def explore_pod() -> list[Resource]:
    resources = []

    async with Client(client.CoreV1Api) as c:
        pods = await explore_pods(c)
        resources.extend(pods)

    return resources


###############################################################################
# Private functions
###############################################################################
async def explore_pods(c: AsyncClient) -> list[Resource]:
    f = "list_pod_for_all_namespaces"
    response = await c.execute(f)

    if response.status == 403:
        logger.warning("Kubernetes API server failed authentication")
        return []

    if response.status == 404:
        logger.warning(f"Kubernetes API server '{f}' not found")
        return []

    pods = msgspec.json.decode(response.data)

    if "items" not in pods:
        logger.warning(f"No pods found: {pods}")
        return []

    results = []
    for pod in pods["items"]:
        meta = pod["metadata"]
        results.append(
            Resource(
                id=make_id(meta["uid"]),
                meta=K8SMeta(
                    name=meta["name"],
                    display=meta["name"],
                    kind="pod",
                    platform="k8s",
                    ns=meta["namespace"],
                    category="compute",
                ),
                struct=pod,
            )
        )

    return results
