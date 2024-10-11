"""
This module provides a client for interacting with the TripIt API.

Classes:
    Session: A session class that combines caching and OAuth1 authentication.
    TripItClient: A client class that provides methods to interact with the TripIt API.

Functions:
    try_float(value: str) -> float: Attempts to convert a string to a float, returning the original value if conversion fails.

TripItClient Methods:
    __init__(
        base_url: URL = "https://api.tripit.com/v1"
        Initializes the TripItClient with the provided tokens and base URL.

    get_info() -> dict:
        Returns a dictionary containing the current timestamp and the client version.

    get_objects(
        *args: URL
        Retrieves objects from the TripIt API based on the provided key and URLs.
"""

import datetime
from collections.abc import Generator
from os import environ
from pathlib import Path
from queue import Queue
from typing import Any

import more_itertools
from alive_progress import alive_bar
from appdirs import user_config_dir
from dotenv import load_dotenv
from requests_cache import CacheMixin
from requests_oauthlib import OAuth1Session
from yarl import URL

from illallangi.tripit.__version__ import __version__
from illallangi.tripit.client.flight import FlightMixin
from illallangi.tripit.client.profile import ProfileMixin
from illallangi.tripit.client.trip import TripMixin

load_dotenv(override=True)

ACCESS_TOKEN = environ.get("TRIPIT_ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET = environ.get("TRIPIT_ACCESS_TOKEN_SECRET", None)
CLIENT_TOKEN = environ.get("TRIPIT_CLIENT_TOKEN", None)
CLIENT_TOKEN_SECRET = environ.get("TRIPIT_CLIENT_TOKEN_SECRET", None)

CACHE_NAME = Path(user_config_dir()) / "illallangi-tripit.db"


class Session(
    CacheMixin,
    OAuth1Session,
):
    """
    Session class that inherits from CacheMixin and OAuth1Session.

    This class is designed to manage sessions with caching and OAuth1 authentication.

    Attributes:
        None

    Methods:
        None
    """


def try_float(
    value: str,
) -> float | str:
    """
    Attempt to convert a string to a float.

    Args:
        value (str): The string value to convert.
    Returns:
        float: The converted float value if successful.
        str: The original string value if conversion fails due to ValueError or TypeError.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return value


class TripItClient(
    FlightMixin,
    ProfileMixin,
    TripMixin,
):
    """
    TripItClient is a client for interacting with the TripIt API. It provides methods to retrieve information about flights, profiles, and trips.

    Attributes:
        base_url (URL): The base URL for the TripIt API.
        _session (Session): The session object for making authenticated requests.
    Methods:
        __init__(access_token: str, access_token_secret: str, client_token: str, client_token_secret: str, base_url: URL) -> None:
            Initializes the TripItClient with the provided tokens and base URL.
        get_info() -> dict:
            Returns a dictionary containing the current timestamp and version information.
        get_objects(key: str, *args: URL) -> Generator[dict[str, Any], None, None]:
            Retrieves objects from the TripIt API based on the provided key and URLs. Yields dictionaries
            containing the object data and additional API metadata.
    """

    def __init__(
        self,
        access_token: str = ACCESS_TOKEN,
        access_token_secret: str = ACCESS_TOKEN_SECRET,
        client_token: str = CLIENT_TOKEN,
        client_token_secret: str = CLIENT_TOKEN_SECRET,
        base_url: URL = "https://api.tripit.com/v1",
    ) -> None:
        """
        Initialize the TripIt client with the given tokens and base URL.

        Args:
            access_token (str): The access token for authentication. Defaults to ACCESS_TOKEN.
            access_token_secret (str): The access token secret for authentication. Defaults to ACCESS_TOKEN_SECRET.
            client_token (str): The client token for authentication. Defaults to CLIENT_TOKEN.
            client_token_secret (str): The client token secret for authentication. Defaults to CLIENT_TOKEN_SECRET.
            base_url (URL or str): The base URL for the TripIt API. Defaults to "https://api.tripit.com/v1".
        Raises:
            TypeError: If base_url is not an instance of URL or a string that can be converted to a URL.
        """
        if not isinstance(base_url, URL):
            base_url = URL(base_url)

        self.base_url = base_url

        self._session = Session(
            client_key=client_token,
            client_secret=client_token_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            cache_name=CACHE_NAME,
            backend="sqlite",
            expire_after=3600,
        )

    def get_info(
        self,
    ) -> dict:
        """
        Retrieve information about the current state of the client.

        Returns:
            dict: A dictionary containing:
                - "returned" (int): The current timestamp in seconds since the epoch.
                - "version" (str): The version of the client.
        """
        return {
            "returned": int(datetime.datetime.now(tz=datetime.UTC).timestamp()),
            "version": __version__,
        }

    def get_objects(
        self,
        key: str,
        *args: URL,
    ) -> Generator[dict[str, Any], None, None]:
        """
        Retrieve objects from the specified URLs.

        This method fetches data from the given URLs, processes the JSON response, and yields dictionaries
        containing the data along with additional metadata.
        Args:
            key (str): The key to extract from the JSON response.
            *args (URL): Variable length argument list of URLs to fetch data from.
        Yields:
            dict[str, Any]: A dictionary containing the data from the JSON response and additional metadata.
        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        queue = Queue()
        seen = set()

        for arg in args:
            seen.add(
                arg
                % {
                    "format": "json",
                    "page_size": 13,
                    "page_num": 1,
                }
            )
            queue.put(
                arg
                % {
                    "format": "json",
                    "page_size": 13,
                    "page_num": 1,
                }
            )

        with alive_bar(manual=True) as bar:
            while not queue.empty():
                url = queue.get()
                bar.text(f"{url.human_repr()}; {queue.qsize()} to go.")

                response = self._session.get(url)

                response.raise_for_status()

                json = response.json()

                yield from [
                    {
                        **o,
                        "@api": {
                            **{
                                k: try_float(v)
                                for k, v in json.items()
                                if k
                                not in [
                                    "AirObject",
                                    "Profile",
                                    "Trip",
                                ]
                            },
                            "from_cache": response.from_cache,
                            "expires": int(response.expires.timestamp()),
                            "url": url.human_repr(),
                            **self.get_info(),
                        },
                    }
                    for o in more_itertools.always_iterable(
                        json.get(key, []),
                        base_type=dict,
                    )
                ]

                if "max_page" in json:
                    for page_num in range(
                        1,
                        int(json["max_page"]) + 1,
                    ):
                        u = url % {
                            "format": "json",
                            "page_size": 13,
                            "page_num": page_num,
                        }
                        if u in seen:
                            continue
                        seen.add(u)
                        queue.put(u)
                bar((len(seen) - queue.qsize()) / len(seen))
