"""Position object definition."""
from __future__ import annotations
from datetime import datetime

from .instrument import Instrument

class Position:
    """Store attributes associated with an account position."""

    def __init__(
        self,
        quantity: float = 0.0,
        average_price: float = 0.0,
        pl: float = 0.0,
        pl_pct: float = 0.0,
        market_value: float = 0.0,
        instrument: Instrument = None
    ):
        """Constructor."""
        self.quantity = quantity
        self.average_price = average_price
        self.pl = pl
        self.pl_pct = pl_pct
        self.market_value = market_value
        self.instrument = instrument

    def __str__(self) -> str:
        """String representation"""
        return f"{self.market_value}"

    def __repr__(self) -> str:
        """String representation"""
        return self.__str__()
