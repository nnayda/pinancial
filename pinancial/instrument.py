"""Instrument object definition."""
from __future__ import annotations
from aenum import Enum

class InstrumentType(Enum):
    """Instrument types"""

    _init_ = 'value string'

    EQUITY = 1, "Equity"
    CASH = 2, "Cash"

    def __str__(self):
        return self.string

class Instrument:
    """Store attributes associated with an instrument"""

    def __init__(
        self,
        type: int,
        cusip: str = "",
        symbol: str = "",
    ):
        """Constructor."""
        self.type = type
        self.cusip = cusip
        self.symbol = symbol

    def __str__(self) -> str:
        """String representation"""
        return f"{self.symbol}"

    def __repr__(self) -> str:
        """String representation"""
        return self.__str__()
