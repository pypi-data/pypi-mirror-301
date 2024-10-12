from collections.abc import Generator
from datetime import datetime, timezone
from typing import Any

import more_itertools

from illallangi.tripit.utils import try_jsonpatch


class FlightMixin:
    def get_flights(
        self,
    ) -> Generator[dict[str, Any], None, None]:
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
        ):
            for segment in [
                try_jsonpatch(
                    segment,
                    segment.get("notes"),
                )
                for segment in more_itertools.always_iterable(
                    air.get("Segment", []),
                    base_type=dict,
                )
            ]:
                yield {
                    "Airline": segment["marketing_airline_code"],
                    "Arrival": datetime.fromisoformat(
                        f'{segment["EndDateTime"]["date"]}T{segment["EndDateTime"]["time"]}{segment["EndDateTime"]["utc_offset"]}',
                    ).astimezone(timezone.utc),
                    "ArrivalTimeZone": segment["EndDateTime"]["timezone"],
                    "Departure": datetime.fromisoformat(
                        f'{segment["StartDateTime"]["date"]}T{segment["StartDateTime"]["time"]}{segment["StartDateTime"]["utc_offset"]}',
                    ).astimezone(timezone.utc),
                    "DepartureTimeZone": segment["StartDateTime"]["timezone"],
                    "Destination": segment.get("end_airport_code"),
                    "DestinationCity": segment["end_city_name"],
                    "DestinationTerminal": segment.get("end_terminal"),
                    "FlightClass": segment.get("service_class"),
                    "FlightNumber": f'{segment["marketing_airline_code"]}{int(segment["marketing_flight_number"])}',
                    "Origin": segment.get("start_airport_code"),
                    "OriginCity": segment["start_city_name"],
                    "OriginTerminal": segment.get("start_terminal"),
                    "@air": {
                        k: v for k, v in air.items() if k not in ["@api", "Segment"]
                    },
                    "@api": air["@api"],
                    "@segment": segment,
                }
