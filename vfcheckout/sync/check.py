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
        product_name: str,
        *,
        user_id: Optional[int] = None,
        guild_id: Optional[int] = None) -> bool:
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

    log.info("Checking purchase with params %s", d(params))
    site = requests.get(
        "https://voxelfox.co.uk/api/portal/check",
        params=params,
    )
    log.info("Response from site: %s", site.text)
    data = site.json()
    return data["result"]
