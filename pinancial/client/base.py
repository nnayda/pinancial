"""Base class for api client"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Callable
from dateutil import parser
import yaml
from pinancial.account import Account, AccountMode, AccountType, AccountStatus
from pinancial.instrument import Instrument, InstrumentType
from pinancial.quote import Quote, EquityQuote
from pinancial.utils import key_found, get_item
from pinancial.position import Position, PositionType

BASE_DIR = Path(__file__).resolve().parent.parent
with open(BASE_DIR / "config" / "utils.yaml", "r") as stream:
    try:
        SETTINGS = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


class Client(ABC):
    """API client."""

    def __init__(self, consumer_key: str, consumer_secret: str):
        """Constructor."""
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.account_map: list = []
        self.accountmode_map: list = []
        self.accounttype_map: list = []
        self.accountstatus_map: list = []
        self.instrument_map: list = []
        self.instrumenttype_map: list = []
        self.equity_map: list = []
        self.positiontype_map: list = []
        self.position_map: list = []
        self.session = None

    def get_session(self, text_code: str = "") -> None:
        """Setup an auth session."""
        self.session = self._oauth.get_auth_session(
            self.request_token,
            self.request_token_secret,
            params={"oauth_verifier": text_code},
        )

    @abstractmethod
    def get_accounts(self) -> list[Account]:
        """Get the accounts for a client."""

    @abstractmethod
    def get_positions(self, account: Account, link: str = None) -> list[Position]:
        """Get the positions for an account."""

    def _parse_account(self, response: dict) -> Optional[Account]:
        """Parse an api response using the defined mapping of keys and types."""
        details = {}
        for item in self.account_map:
            if key_found(response, *item["from"].split(".")):
                val = get_item(response, *item["from"].split("."))
                try:
                    val = self._convert_val(val, item["type"])

                except ValueError:
                    break

                details[item["to"]] = val

        if len(details) > 0:
            return Account(**details)

        return None

    def _parse_instrument(self, response: dict) -> Optional[Instrument]:
        """Parse an api response using defined mapping of keys and types."""
        details = {}

        for item in self.instrument_map:
            if key_found(response, *item["from"].split(".")):
                val = get_item(response, *item["from"].split("."))
                try:
                    val = self._convert_val(val, item["type"])

                except ValueError:
                    break

                details[item["to"]] = val

        if len(details) > 0:
            return Instrument(**details)

        return None

    def _parse_position(self, response: dict) -> Optional[Position]:
        """Parse an api response using defined mapping of keys and types."""
        details = {}
        for item in self.position_map:
            if key_found(response, *item["from"].split(".")):
                val = get_item(response, *item["from"].split("."))
                try:
                    val = self._convert_val(val, item["type"])

                except ValueError:
                    break

                details[item["to"]] = val

        if len(details) > 0:
            details["instrument"] = self._parse_instrument(response)
            return Position(**details)

        return None

    def _parse_quote(self, response: dict) -> Optional[Quote]:
        """Parse an api response using defined mapping of keys and types."""
        details = {}

        instrument = self._parse_instrument(response)
        if instrument is not None and instrument.inst_type == InstrumentType.EQUITY:
            mapping = self.equity_map
        for item in mapping:
            if key_found(response, *item["from"].split(".")):
                val = get_item(response, *item["from"].split("."))
                try:
                    val = self._convert_val(val, item["type"])

                except ValueError:
                    break

                details[item["to"]] = val

        if len(details) > 0:
            details["instrument"] = instrument
            return EquityQuote(**details)

        return None

    def _convert_val(self, val: Any, val_type: str) -> Any:
        """Convert a value to the defined type."""
        conversions: dict[str, Callable] = {
            "str": str,
            "int": int,
            "float": float,
            "timestamp": lambda x: None if x == 0 else datetime.fromtimestamp(x / 1000),
            "datetime": lambda x: parser.parse(x, tzinfos=SETTINGS["tzinfo"]),
            "AccountMode": lambda x: AccountMode[self.accountmode_map[x]],
            "AccountType": lambda x: AccountType[self.accounttype_map[x]],
            "AccountStatus": lambda x: AccountStatus[self.accountstatus_map[x]],
            "PositionType": lambda x: PositionType[self.positiontype_map[x]],
            "InstrumentType": lambda x: InstrumentType[self.instrumenttype_map[x]],
        }
        return conversions[val_type](val)
