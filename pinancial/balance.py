"""Balance object definition."""
from __future__ import annotations
from datetime import date


class Balance:
    """Store attributes associated with an account balance."""

    def __init__(
        self,
        market_value: float = 0,
        cash: float = 0,
        invested: float = 0,
        margin: float = 0,
        as_of_date: date = None,
    ):
        """Constructor."""
        self.market_value = market_value
        self.cash = cash
        self.invested = invested
        self.margin = margin
        self.as_of_date = as_of_date
