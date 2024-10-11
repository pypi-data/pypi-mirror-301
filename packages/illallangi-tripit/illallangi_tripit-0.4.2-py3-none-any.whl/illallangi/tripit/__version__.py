"""
This module defines the version information for the TripIt package.

Attributes:
    __version__ (str): The current version of the TripIt package.
    __version_info__ (tuple): A tuple containing the major, minor, and patch version numbers.
"""

__version__ = "0.4.2"
__version_info__ = tuple(map(int, __version__.split("+")[0].split(".")))
