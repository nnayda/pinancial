"""Balance object definition."""
from __future__ import annotations
from datetime import datetime


class Balance:
    """Store attributes associated with an account balance."""

    def __init__(
        self,
        accrued_interest: float = 0.0,
        cash: float = 0.0,
        long_option_value: float = 0.0,
        market_value: float = 0.0,
        long_market_value: float = 0.0,
        short_market_value: float = 0.0,
        pending_deposits: float = 0.0,
        short_option_value: float = 0.0,
        unsettled_cash: float = 0.0,
    
    ):
        """Constructor."""
        self.accrued_interest = accrued_interest
        self.cash = cash
        self.long_option_value = long_option_value
        self.market_value = market_value
        self.long_market_value = long_market_value
        self.short_market_value = short_market_value
        self.pending_deposits = pending_deposits
        self.short_option_value = short_option_value
        self.unsettled_cash = unsettled_cash
        self.as_of = datetime.now()

    def __str__(self) -> str:
        """String representation"""
        return f"{self.market_value}"

    def __repr__(self) -> str:
        """String representation"""
        return self.__str__()
