"""
Retrieve profiles from the API.

This method yields profiles as dictionaries containing the following keys:
- "ID": The unique identifier of the profile.
- "Name": The public display name of the profile.
- "Company": The company associated with the profile.
- "Location": The home city of the profile.
- "@api": API-specific metadata for the profile.
- "@profile": A dictionary of profile attributes excluding the "@api" key.

Yields:
    dict[str, Any]: A dictionary representing a profile.
"""

from collections.abc import Generator
from typing import Any


class ProfileMixin:
    """A mixin class to handle profile-related operations."""

    def get_profiles(
        self,
    ) -> Generator[dict[str, Any], None, None]:
        """
        Retrieve profiles from the TripIt API.

        This method yields dictionaries containing profile information. Each dictionary
        includes the following keys:
        - "ID": The unique identifier of the profile.
        - "Name": The public display name of the profile.
        - "Company": The company associated with the profile.
        - "Location": The home city of the profile.
        - "@api": API-specific information related to the profile.
        - "@profile": A dictionary containing all other profile information except "@api".
        Yields:
            Generator[dict[str, Any], None, None]: A generator yielding dictionaries with profile information.
        """
        yield from [
            {
                "ID": profile["uuid"],
                "Name": profile["public_display_name"],
                "Company": profile["company"],
                "Location": profile["home_city"],
                "@api": profile["@api"],
                "@profile": {k: v for k, v in profile.items() if k not in ["@api"]},
            }
            for profile in self.get_objects(
                "Profile",
                self.base_url / "get" / "profile",
            )
        ]
