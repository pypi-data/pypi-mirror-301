# mypy: disable-error-code="call-arg,index"
import logging

import httpx
import msgspec

from lueur.make_id import make_id
from lueur.models import Meta, Resource

__all__ = ["explore_flow_dependencies"]
logger = logging.getLogger("lueur.lib")


async def explore_flow_dependencies(k8packet_address: str) -> list[Resource]:
    resource = await explore_k8packet(k8packet_address)
    if not resource:
        return []

    return [resource]


###############################################################################
# Private functions
###############################################################################
async def explore_k8packet(k8packet_address: str) -> Resource | None:
    async with httpx.AsyncClient(base_url=k8packet_address) as c:
        response = await c.get("/nodegraph/api/graph/fields")

        if response.status_code == 404:
            logger.warning("k8spacket not found. Please install k8packet")
            return None

        fields = msgspec.json.decode(response.content)

        response = await c.get("/nodegraph/api/graph/data")

        if response.status_code == 404:
            logger.warning("k8spacket not found. Please install k8packet")
            return None

        data = msgspec.json.decode(response.content)

        return Resource(
            id=make_id(k8packet_address),
            meta=Meta(
                name="flow-dependency",
                display="Flow Dependency",
                kind="dependency",
                platform="k8s",
                category="network",
            ),
            struct={"fields": fields, "graph": data},
        )
