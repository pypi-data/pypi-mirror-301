"""
FlightMixin class provides functionality to retrieve flight information.

Methods:
    get_flights() -> Generator[dict[str, Any], None, None]:
        Yields flight information as dictionaries containing details such as
        origin, destination, departure, arrival, and additional metadata.

        Yields:
            dict: A dictionary containing flight details:
                - "Origin": The starting airport code.
                - "Destination": The ending airport code.
                - "Departure": The departure date and time in ISO 8601 format.
                - "Arrival": The arrival date and time in ISO 8601 format.
                - "@air": Additional flight information excluding "@api" and "Segment".
                - "@api": API-related metadata.
                - "@segment": The segment information of the flight.
"""

from collections.abc import Generator
from datetime import datetime, timezone
from typing import Any

import more_itertools


class FlightMixin:
    """
    A mixin class to provide functionality for retrieving flight information.

    Methods
    -------
    get_flights() -> Generator[dict[str, Any], None, None]:
        Yields dictionaries containing flight details such as origin, destination,
        departure time, arrival time, and other relevant information.
    """

    def get_flights(
        self,
    ) -> Generator[dict[str, Any], None, None]:
        """
        Retrieve flight information from the API and yields it as a generator of dictionaries.

        Yields:
            Generator[dict[str, Any], None, None]: A generator that yields dictionaries containing flight details.
                Each dictionary contains the following keys:
                    - "Origin": The starting airport code of the flight segment.
                    - "Destination": The ending airport code of the flight segment.
                    - "Departure": The departure date and time in ISO 8601 format.
                    - "Arrival": The arrival date and time in ISO 8601 format.
                    - "@air": A dictionary of air object details excluding "@api" and "Segment".
                    - "@api": The API details of the air object.
                    - "@segment": The segment details of the flight.
        """
        yield from [
            {
                "Origin": segment.get("start_airport_code"),
                "Destination": segment.get("end_airport_code"),
                "Departure": datetime.fromisoformat(
                    f'{segment["StartDateTime"]["date"]}T{segment["StartDateTime"]["time"]}{segment["StartDateTime"]["utc_offset"]}',
                ).astimezone(timezone.utc),
                "DepartureTimeZone": segment["StartDateTime"]["timezone"],
                "Arrival": datetime.fromisoformat(
                    f'{segment["EndDateTime"]["date"]}T{segment["EndDateTime"]["time"]}{segment["EndDateTime"]["utc_offset"]}',
                ).astimezone(timezone.utc),
                "ArrivalTimeZone": segment["EndDateTime"]["timezone"],
                "@air": {k: v for k, v in air.items() if k not in ["@api", "Segment"]},
                "@api": air["@api"],
                "@segment": segment,
            }
            for air in self.get_objects(
                "AirObject",
                self.base_url
                / "list"
                / "object"
                / "traveler"
                / "true"
                / "past"
                / "true"
                / "include_objects"
                / "false"
                / "type"
                / "air",
                self.base_url
                / "list"
                / "object"
                / "traveler"
                / "true"
                / "past"
                / "false"
                / "include_objects"
                / "false"
                / "type"
                / "air",
            )
            for segment in more_itertools.always_iterable(
                air.get("Segment", []),
                base_type=dict,
            )
        ]
