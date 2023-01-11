from collections.abc import Awaitable, Callable
import logging
from typing import Any, Optional, TypeVar
import json

import aiohttp


log = logging.getLogger("vfcheckout.async")
d = json.dumps


__all__ = (
    'check',
)


async def check(
        product_name: str,
        *,
        user_id: Optional[int] = None,
        guild_id: Optional[int] = None,
        session: Optional[aiohttp.ClientSession] = None) -> bool:
    """
    Check if a given user/guild has an active purchase for the given product.
    """

    if user_id is not None and guild_id is not None:
        raise ValueError("Only one of user_id or guild_id can be provided.")
    params: dict[str, Any] = {
        "product_name": product_name,
    }
    if user_id is not None:
        params["user_id"] = user_id
    elif guild_id is not None:
        params["guild_id"] = guild_id
    args = {
        "url": "https://voxelfox.co.uk/api/portal/check",
        "params": params,
    }

    log.info("Checking purchase with params %s", d(params))
    if session is None:
        async with aiohttp.ClientSession() as session:
            site = await session.get(**args)
    else:
        site = await session.get(**args)
    log.info("Response from site: %s", await site.text())
    data = await site.json()
    return data["result"]
