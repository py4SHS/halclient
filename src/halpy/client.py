from __future__ import annotations

import datetime
from enum import Enum
from urllib.parse import urljoin

import httpx


class Order(str, Enum):
    """Allowed sorting oders when interacting with HAL API."""

    ASCENDING = "asc"
    DESCENDING = "desc"


class Format(str, Enum):
    """Allowed formats when interacting with HAL API.

    This class is an "Enumeration".

    Because it is easy to make errors when writing strings manually,
    enumerations can be used to detect errors earlier and explicitely
    describe to end-users the allowed choices for a given operation.

    Any time you have a given set of constants (fixed values), you SHOULD
    use enums.

    Reference: https://api.archives-ouvertes.fr/docs/search#Formats%20de%20r%C3%A9ponse:~:text=Histoire%20OR%20History)-,Formats%20de%20r%C3%A9ponse,-Le%20format%20de
    """

    JSON = "json"
    XML = "xml"
    XML_TEI = "xml-tei"
    BIBTEX = "bibtex"
    CSV = "csv"


class HALClient:
    """A Python client to interact with HAL API.

    Reference: https://api.archives-ouvertes.fr/docs/search
    """

    def __init__(
        self,
        portal: str | None = None,
        collection: str | None = None,
        default_format: Format = Format.JSON,
        timeout: float = 60,
        base_url: str = "http://api.archives-ouvertes.fr/search/",
    ):
        """Create a new instance of HALClient.

        Arguments:
            portal: HAL API exists for several portals, you can choose which portal you want to use. By default the global portal is used.
            collection: Limit the search to a specific collection.
            default_format: Choose the default output format for all requests.
            timeout: Choose the duration to wait for each request to succeed. Requests are cancelled if they do not succeed before timeout.
            base_url: The base URL where requests should be sent. Users do not need to change the default value most of the time.
        """
        if collection and portal:
            raise ValueError(
                "Either 'portail' or 'collection' parameter can be provided, but not both at the same time."
            )
        # It's a good practice to store the user provided configuration
        self.collection = collection
        self.portal = portal
        self.default_format = default_format
        # Build the URL where requests should be sent
        if self.portal:
            base_url = urljoin(base_url, portal)
        elif self.collection:
            base_url = urljoin(base_url, collection)
        # Create an HTTP client. This object will be used to send requests to the HAL API.
        self.client = httpx.Client(base_url=base_url, timeout=timeout)

    def search(
        self,
        query: str,
        format: Format | None = None,
        include_fields: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: Order | None = None,
        before: int | None = None,
        after: int | None = None,
        rows: int = 0,
        offset: int = 0,
    ):
        params: dict[str, str | int] = {
            "q": query,
            "wt": Format(format).value if format else self.default_format.value,
        }
        if include_fields:
            params["fl"] = ",".join(include_fields)
        if sort_by:
            order = Order(sort_order) if sort_order else Order.ASCENDING
            params["sort"] = f"{sort_by} {order.value}"
        if after or before:
            after = after or datetime.datetime.now().year
            before = before or 1900
            params["fq"] = f"submittedDateY_i:[{after} TO {before}}}"
        params["rows"] = rows
        params["start"] = offset
        response = self.client.get("/", params=params)
        print(response.request.url)
        response.raise_for_status()
        return response
