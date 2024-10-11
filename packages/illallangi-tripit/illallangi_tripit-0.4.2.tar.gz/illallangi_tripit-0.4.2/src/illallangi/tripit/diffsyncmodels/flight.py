"""Flight is a DiffSyncModel that represents a flight record in a TripIt application."""

from datetime import datetime

import diffsync


class Flight(diffsync.DiffSyncModel):
    """
    Flight is a DiffSyncModel that represents a flight activity.

    Attributes:
        url (str): URL identifier for the flight record.
        content (str): Content of the flight.
        datetime (str): Date and Time of the flight.
    Class Attributes:
        _modelname (str): Name of the model.
        _identifiers (tuple): Identifiers for the model.
        _attributes (tuple): Attributes of the model.
    Methods:
        create(cls, adapter, ids, attrs):
            Creates or updates a flight record in the database and returns the created item.
            Args:
                adapter: The adapter instance.
                ids (dict): Dictionary containing the identifiers.
                attrs (dict): Dictionary containing the attributes.
            Returns:
                Flight: The created or updated flight item.
        update(self, attrs):
            Updates the flight record in the database with the given attributes.
            Args:
                attrs (dict): Dictionary containing the attributes to update.
            Returns:
                Flight: The updated flight item.
        delete(self):
            Deletes the flight record from the database.
            Returns:
                Flight: The deleted flight item.
    """

    _modelname = "Flight"
    _identifiers = (
        "departure",
        "origin",
    )
    _attributes = (
        "arrival_timezone",
        "arrival",
        "departure_timezone",
        "destination",
    )

    arrival_timezone: str
    arrival: datetime
    departure_timezone: str
    departure: datetime
    destination: str
    origin: str

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Flight":
        """
        Create a Flight instance.

        This method updates or creates a ModelFlight object using the provided ids and attrs,
        then creates a Flight instance with the updated or created ModelFlight object's
        primary key and the provided ids and attrs.
        Args:
            cls: The class that this method is called on.
            adapter: The adapter to use for creating the Flight instance.
            ids (dict): A dictionary containing the identifiers for the ModelFlight object.
            attrs (dict): A dictionary containing the attributes for the ModelFlight object.
        Returns:
            Flight: The created Flight instance.
        """
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Flight":
        """
        Update the current Flight instance with the provided attributes.

        Args:
            attrs (dict): A dictionary of attributes to update the instance with.
        Returns:
            Flight: The updated Flight instance.
        """
        raise NotImplementedError

    def delete(
        self,
    ) -> "Flight":
        """
        Delete the current Flight instance from the database.

        This method first deletes the associated ModelFlight object using its primary key (pk),
        and then calls the superclass's delete method to remove the Flight instance.
        Returns:
            Flight: The deleted Flight instance.
        """
        raise NotImplementedError
