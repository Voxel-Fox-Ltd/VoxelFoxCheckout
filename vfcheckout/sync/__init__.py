from __future__ import annotations

import logging
from typing import Any, Optional
import json

import requests


log = logging.getLogger("vfcheckout.sync")
d = json.dumps


__all__ = (
    'check',
)


def check(
        *,
        product_name: str | None = None,
        product_id: str | None = None,
        user_id: Optional[int] = None,
        guild_id: Optional[int] = None) -> bool:
    """
    Check if a given user/guild has an active purchase for the given product.
    """

    params: dict[str, Any] = {}

    if user_id is not None and guild_id is not None:
        raise ValueError("Only one of user_id or guild_id can be provided.")

    if product_name is not None and product_id is not None:
        raise ValueError("Only one of user_id or guild_id can be provided.")
    elif product_name is None and product_id is None:
        raise ValueError("Only one of user_id or guild_id can be provided.")
    elif product_name:
        params["product_name"] = product_name
    elif product_id:
        params["product_id"] = product_id

    if user_id is not None:
        params["user_id"] = user_id
    elif guild_id is not None:
        params["guild_id"] = guild_id

    args = {
        "url": "https://voxelfox.co.uk/api/portal/check",
        "params": params,
    }

    log.info("Checking purchase with params %s", d(params))
    try:
        site = requests.get(
            **args,
            timeout=1.5,
        )
    except Exception as e:
        log.error("Error checking purchase: %s", e)
        return False
    log.info("Response from site: %s", site.text)
    data = site.json()
    return data["result"]
