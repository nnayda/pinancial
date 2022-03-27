"""Etrade client."""
from __future__ import annotations
from pathlib import Path
from rauth import OAuth1Service
from pinancial.exceptions import (
    Error400,
    Error401,
    Error403,
    Error404,
    Error415,
    Error423,
    Error500,
)
from pinancial.client import Client
from pinancial.account import Account
from pinancial.quote import Quote
from pinancial.position import Position
from pinancial.utils import get_settings

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS = get_settings(BASE_DIR / "config" / "etrade.yaml")


class EtradeClient(Client):
    """Etrade api client"""

    def __init__(self, consumer_key: str, consumer_secret: str):
        """Constructor"""
        super().__init__(consumer_key, consumer_secret)
        self.base_url = "https://api.etrade.com"
        self.session = None
        self._oauth: OAuth1Service = OAuth1Service(
            name="etrade",
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            request_token_url="https://api.etrade.com/oauth/request_token",
            access_token_url="https://api.etrade.com/oauth/access_token",
            authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
            base_url=self.base_url,
        )
        self.request_token, self.request_token_secret = self._oauth.get_request_token(
            params={"oauth_callback": "oob", "format": "json"}
        )
        self.authorize_url = self._oauth.authorize_url.format(
            self.consumer_key, self.request_token
        )
        self.account_map = SETTINGS["account_map"]
        self.accountmode_map = SETTINGS["account_mode_map"]
        self.accounttype_map = SETTINGS["account_type_map"]
        self.accountstatus_map = SETTINGS["account_status_map"]
        self.instrument_map = SETTINGS["instrument_map"]
        self.instrumenttype_map = SETTINGS["instrument_type_map"]
        self.equity_map = SETTINGS["equity_map"]
        self.position_map = SETTINGS["position_map"]
        self.positiontype_map = SETTINGS["position_type_map"]

    def get_accounts(self) -> list[Account]:
        """Get all accounts."""
        parsed_accounts = []
        response = self.session.get(
            self.base_url + "/v1/accounts/list.json", header_auth=True
        )
        # Parse response
        if response is not None and response.status_code == 200:
            data = response.json()
            if (
                data is not None
                and "AccountListResponse" in data
                and "Accounts" in data["AccountListResponse"]
                and "Account" in data["AccountListResponse"]["Accounts"]
            ):
                accounts = data["AccountListResponse"]["Accounts"]["Account"]
                accounts[:] = [
                    d for d in accounts if d.get("accountStatus") != "CLOSED"
                ]
                for account in accounts:
                    parsed_account = self._parse_account(account)
                    if parsed_account:
                        parsed_accounts.append(parsed_account)

                return parsed_accounts

        _handle_errors(response)
        return []

    def get_positions(self, account: Account, link: str = None) -> list[Position]:
        """Get all positions for an account."""
        positions = []
        if link is not None:
            response = self.session.get(link, header_auth=True)
        else:
            response = self.session.get(
                self.base_url + f"/v1/accounts/{account.account_key}/portfolio.json",
                header_auth=True,
            )

        # Parse response
        if response is not None and response.status_code == 200:
            data = response.json()
            if (
                data is not None
                and "PortfolioResponse" in data
                and "AccountPortfolio" in data["PortfolioResponse"]
                and "Position" in data["PortfolioResponse"]["AccountPortfolio"][0]
            ):
                position_data = data["PortfolioResponse"]["AccountPortfolio"][0][
                    "Position"
                ]
                for position in position_data:
                    parsed_position = self._parse_position(position)
                    if parsed_position:
                        positions.append(parsed_position)
                if "next" in data["PortfolioResponse"]["AccountPortfolio"][0]:
                    positions.extend(
                        self.get_positions(
                            account,
                            data["PortfolioResponse"]["AccountPortfolio"][0]["next"],
                        )
                    )

                return positions

        _handle_errors(response)
        return []

    def get_quotes(self, symbols: list[str]) -> list[Quote]:
        """Get quotes for a list of symbols."""
        parsed_quotes = []
        response = self.session.get(
            f"{self.base_url}/v1/market/quote/{','.join(symbols)}.json",
            header_auth=True,
        )
        # Parse response
        if response is not None and response.status_code == 200:
            data = response.json()
            if (
                data is not None
                and "QuoteResponse" in data
                and "QuoteData" in data["QuoteResponse"]
            ):
                for quote in data["QuoteResponse"]["QuoteData"]:
                    parsed_quote = self._parse_quote(quote)
                    if parsed_quote:
                        parsed_quotes.append(parsed_quote)

                return parsed_quotes

        _handle_errors(response)
        return []


def _handle_errors(response: dict) -> None:
    """Handle errors retrieving data from api."""
    if (
        response is not None
        and response.headers["Content-Type"] == "application/json"
        and "Error" in response.json()
        and "message" in response.json()["Error"]
        and response.json()["Error"]["message"] is not None
    ):
        if response.status_code == 400:
            raise Error400(response.json()["Error"]["message"])
        if response.status_code == 401:
            raise Error401(response.json()["Error"]["message"])
        if response.status_code == 403:
            raise Error403(response.json()["Error"]["message"])
        if response.status_code == 404:
            raise Error404(response.json()["Error"]["message"])
        if response.status_code == 415:
            raise Error415(response.json()["Error"]["message"])
        if response.status_code == 423:
            raise Error423(response.json()["Error"]["message"])
    raise Error500("AccountList API service error")
