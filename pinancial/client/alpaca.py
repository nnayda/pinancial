"""Alpaca client."""
from __future__ import annotations
from pathlib import Path
import alpaca_trade_api as tradeapi
from pinancial.client import Client
from pinancial.account import Account
from pinancial.position import Position
from pinancial.utils import get_settings

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS = get_settings(BASE_DIR / "config" / "alpaca.yaml")


class AlpacaClient(Client):
    """Alpaca api client"""

    def __init__(self, consumer_key: str, consumer_secret: str):
        """Constructor"""
        super().__init__(consumer_key, consumer_secret)
        self.base_url = "https://api.alpaca.markets"
        self.session = tradeapi.REST(
            self.consumer_key, self.consumer_secret, self.base_url
        )
        self.account_map = SETTINGS["account_map"]
        self.accountmode_map = SETTINGS["account_mode_map"]
        self.accounttype_map = SETTINGS["account_type_map"]
        self.accountstatus_map = SETTINGS["account_status_map"]
        # self.instrument_map = SETTINGS["instrument_map"]
        # self.instrumenttype_map = SETTINGS["instrument_type_map"]
        # self.equity_map = SETTINGS["equity_map"]
        self.name = "Alpaca"

    def get_accounts(self) -> list[Account]:
        """Get all accounts."""
        parsed_accounts = []
        response = self.session.get_account()
        # Parse response
        if response:
            parsed_account = self._parse_account(response.__dict__["_raw"])
            if parsed_account:
                parsed_accounts.append(parsed_account)

        return parsed_accounts

    def get_positions(self, account: Account, link: str = None) -> list[Position]:
        """Get the positions for an account."""
        parsed_positions = []
        response = self.session.list_positions()
        # Parse response
        if response:
            parsed_position = self._parse_position(response.__dict__["_raw"])
            if parsed_position:
                parsed_positions.append(parsed_position)

        return parsed_positions
