"""Define position details for a given account."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from .instrument import Instrument


class PositionType(Enum):
    """Available position types."""

    LONG = "Long"
    SHORT = "Short"
    OTHER = "Other"


class Position:
    """Account position."""

    def __init__(
        self,
        instrument: Instrument,
        date_aquired: datetime = None,
        avg_purchase_price: float = 0,
        commisions: float = 0,
        fees: float = 0,
        avg_cost: float = 0,
        total_cost: float = 0,
        market_value: float = 0,
        quantity: float = 0,
        position_type: PositionType = PositionType.OTHER,
        days_gain: float = 0,
        days_gain_pct: float = 0,
        total_gain: float = 0,
        total_gain_pct: float = 0,
        pct_of_portfolio: float = 0,
        # quote: Quote = None,
    ):
        """Constructor."""
        # Instrument of position held
        self.instrument = instrument
        # Date the position was aquired
        self.date_aquired = date_aquired
        # Average purchase price
        self.avg_purchase_price = avg_purchase_price
        # Commisions paid
        self.commisions = commisions
        # Fees paid
        self.fees = fees
        # Average cost per share
        self.avg_cost = avg_cost
        # Total cost
        self.total_cost = total_cost
        # Current market value
        self.market_value = market_value
        # Number of shares
        self.quantity = quantity
        # Type of position
        self.position_type = position_type
        # Today's gain
        self.days_gain = days_gain
        # Today's gain percentage
        self.days_gain_pct = days_gain_pct
        # Total gain
        self.total_gain = total_gain
        # Total gain percentage
        self.total_gain_pct = total_gain_pct
        # Percentage of portfolio
        self.pct_of_portfolio = pct_of_portfolio
