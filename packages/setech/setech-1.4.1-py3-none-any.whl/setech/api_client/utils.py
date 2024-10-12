import httpx
from httpx._client import USER_AGENT

import setech

_LIB_USER_AGENT = f"Setech Utils v{setech.__version__} ({USER_AGENT})"


def get_httpx_client(
    *,
    sync: bool,
    base_url: str,
    to_read: float | int = 120,
    to_write: float | int = 120,
    user_agent: str | None = _LIB_USER_AGENT,
) -> httpx.Client | httpx.AsyncClient:
    """Method to generate a httpx Client instance to use for setech API Clients.

    :param sync: Should the return be a httpx.Client or httpx.AsyncClient
    :param base_url: Base URL to use for requests
    :param to_read: Seconds to wait for reading responses
    :param to_write: Seconds to wait for writing responses
    :param user_agent: User Agent string to use
    :return: httpx Client instance
    """
    _class = httpx.Client if sync is True else httpx.AsyncClient
    return _class(
        base_url=base_url,
        http2=True,
        timeout=httpx.Timeout(60, read=to_read, write=to_write),
        headers={"user-Agent": user_agent},
    )
