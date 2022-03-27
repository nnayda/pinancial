"""Instrument model definition."""
from __future__ import annotations
from enum import Enum


class InstrumentType(Enum):
    """Available instrument types."""

    EQUITY = "Equity"
    OPTION = "Option"
    MUTUAL_FUND = "Mutual Fund"
    BOND = "Bond"
    CD = "CD"
    OTHER = "Other"


class Instrument:
    """Instrument."""

    def __init__(
        self,
        symbol: str,
        name: str = "",
        description: str = "",
        inst_type: InstrumentType = InstrumentType.OTHER,
    ):
        """Constructor."""

        # ID of the instrument
        self.symbol = symbol
        # Description of the security; for example, the company name or the option description
        self.description = description
        # Name of the company or mutual fund (shows up to 40 characters)
        self.name = name
        # The type of instrument
        self.inst_type = inst_type
