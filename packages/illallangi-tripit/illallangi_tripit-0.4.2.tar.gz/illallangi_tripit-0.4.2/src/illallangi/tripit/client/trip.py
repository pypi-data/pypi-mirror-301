"""A mixin class to provide functionality for retrieving trip information."""

from collections.abc import Generator
from typing import Any


class TripMixin:
    """A mixin class to provide functionality for retrieving trip information."""

    def get_trips(
        self,
    ) -> Generator[dict[str, Any], None, None]:
        """
        Retrieve a list of trips.

        This method yields dictionaries containing trip information. Each dictionary
        includes the trip ID, name, API metadata, and other trip details excluding the API metadata.
        Yields:
            dict[str, Any]: A dictionary with the following keys:
                - "ID": The trip ID.
                - "Name": The display name of the trip.
                - "@api": API metadata associated with the trip.
                - "@trip": A dictionary of trip details excluding the API metadata.
        """
        yield from [
            {
                "ID": trip["id"],
                "Name": trip["display_name"],
                "@api": trip["@api"],
                "@trip": {k: v for k, v in trip.items() if k not in ["@api"]},
            }
            for trip in self.get_objects(
                "Trip",
                self.base_url
                / "list"
                / "trip"
                / "traveler"
                / "true"
                / "past"
                / "true"
                / "include_objects"
                / "false",
                self.base_url
                / "list"
                / "trip"
                / "traveler"
                / "true"
                / "past"
                / "false"
                / "include_objects"
                / "false",
            )
        ]
