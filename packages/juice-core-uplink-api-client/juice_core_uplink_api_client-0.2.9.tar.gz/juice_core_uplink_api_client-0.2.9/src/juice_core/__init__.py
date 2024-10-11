"""
This module provides the core functionality of the Juice Core Uplink API Client
in a more convenient way than the generated code.

May functionalities are not yet implemented, but some are.
"""

from loguru import logger as log

log.disable("juice_core")

from importlib_metadata import version

__version__ = version("juice_core_uplink_api_client")


from .SHTRestInterface import SHTRestInterface, expand_column
