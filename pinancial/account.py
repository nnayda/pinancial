"""Account model definition."""
from __future__ import annotations
from enum import Enum
from datetime import date

from .broker import Broker

class AccountStatus(Enum):
    """Status of the account."""

    ACTIVE = "Active"
    CLOSED = "Closed"


class Account:
    """Financial Account."""

    def __init__(
        self,
        account_id: str,
        broker: Broker,
        account_key: str = "",
        description: str = "",
        name: str = "",
        acct_type: str = "",
        status: AccountStatus = AccountStatus.ACTIVE,
        opened_date: date = None,
        closed_date: date = None,
    ):
        """Constructor"""
        self.account_id = account_id
        self._broker = broker
        self.account_key = account_key
        self.description = description
        self.name = name
        self.acct_type = acct_type
        self.status = status
        self.opened_date = opened_date
        self.closed_date = closed_date

    def __str__(self) -> str:
        return f"<Account: {self.account_id}>"

    def __repr__(self) -> str:
        return self.__str__()


class InvestmentAccount(Account):
    """Investment Account"""

    def __init__(
        self,
        is_day_trader: bool = False,
        is_closing_only_restricted: bool = False,
        **kwargs: dict,
    ):
        """Constructor"""
        super().__init__(**kwargs)
        self.is_day_trader = is_day_trader
        self.is_closing_only_restricted = is_closing_only_restricted
