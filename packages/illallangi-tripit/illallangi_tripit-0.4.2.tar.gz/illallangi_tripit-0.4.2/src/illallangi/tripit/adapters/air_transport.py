"""AirTransportAdapter is a custom adapter for syncing tripit data using the diffsync library."""

from typing import ClassVar

import diffsync

from illallangi.tripit import TripItClient
from illallangi.tripit.diffsyncmodels import Flight


class AirTransportAdapter(diffsync.Adapter):
    """
    AirTransportAdapter is an adapter for syncing Flight objects from a TripIt model.

    Attributes:
        Flight (class): The Flight class to be used for creating Flight objects.
        top_level (list): A list containing the top-level object types.
        type (str): The type identifier for this adapter.
    Methods:
        load():
            Loads Flight objects from the TripIt model and adds them to the adapter.
    """

    Flight = Flight

    top_level: ClassVar = [
        "Flight",
    ]

    type = "tripit_tripit"

    def load(
        self,
    ) -> None:
        """
        Load all Flight objects from the fediverse and adds them to the current instance.

        This method retrieves all trips from the fediverse, converts them into Flight
        objects, and adds them to the current instance.
        Returns:
            None
        """
        for obj in TripItClient().get_flights():
            if (
                not obj["Arrival"]
                or not obj["ArrivalTimeZone"]
                or not obj["Departure"]
                or not obj["DepartureTimeZone"]
                or not obj["Destination"]
                or not obj["Origin"]
            ):
                continue
            self.add(
                Flight(
                    arrival=obj["Arrival"],
                    arrival_timezone=obj["ArrivalTimeZone"],
                    departure=obj["Departure"],
                    departure_timezone=obj["DepartureTimeZone"],
                    destination=obj["Destination"],
                    origin=obj["Origin"],
                ),
            )
