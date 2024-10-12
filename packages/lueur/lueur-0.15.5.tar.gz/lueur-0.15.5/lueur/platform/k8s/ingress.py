# mypy: disable-error-code="call-arg"
import logging

import msgspec
from kubernetes import client

from lueur.make_id import make_id
from lueur.models import K8SMeta, Resource
from lueur.platform.k8s.client import AsyncClient, Client

__all__ = ["explore_ingress"]
logger = logging.getLogger("lueur.lib")


async def explore_ingress() -> list[Resource]:
    resources = []

    async with Client(client.NetworkingV1Api) as c:
        ingresses = await explore_ingresses(c)
        resources.extend(ingresses)

    return resources


###############################################################################
# Private functions
###############################################################################
async def explore_ingresses(c: AsyncClient) -> list[Resource]:
    response = await c.execute("list_ingress_for_all_namespaces")

    ingresses = msgspec.json.decode(response.data)

    if response.status == 403:
        logger.warning(f"K8S API server access failure: {ingresses}")
        return []

    if "items" not in ingresses:
        logger.warning(f"No ingresses found: {ingresses}")
        return []

    results = []
    for ingress in ingresses["items"]:
        meta = ingress["metadata"]
        results.append(
            Resource(
                id=make_id(meta["uid"]),
                meta=K8SMeta(
                    name=meta["name"],
                    display=meta["name"],
                    kind="ingress",
                    platform="k8s",
                    ns=meta["namespace"],
                    category="loadbalancer",
                ),
                struct=ingress,
            )
        )

    return results
