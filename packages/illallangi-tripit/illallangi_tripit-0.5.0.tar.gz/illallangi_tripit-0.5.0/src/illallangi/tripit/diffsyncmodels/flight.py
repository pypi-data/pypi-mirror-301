from datetime import datetime

import diffsync


class Flight(diffsync.DiffSyncModel):
    _modelname = "Flight"
    _identifiers = (
        "departure",
        "flight_number",
    )
    _attributes = (
        "airline",
        "arrival",
        "arrival_timezone",
        "departure_timezone",
        "destination",
        "destination_city",
        "destination_terminal",
        "flight_class",
        "origin",
        "origin_city",
        "origin_terminal",
    )

    airline: str
    arrival: datetime
    arrival_timezone: str
    departure: datetime
    departure_timezone: str
    destination: str
    destination_city: str
    destination_terminal: str | None
    flight_class: str | None
    flight_number: str
    origin: str
    origin_city: str
    origin_terminal: str | None

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Flight":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Flight":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Flight":
        raise NotImplementedError
