'''TD Ameritrade client."""

from __future__ import annotations
from pathlib import Path
from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Client
from tda import auth, client
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
SETTINGS = get_settings(BASE_DIR / "config" / "tda.yaml")


class TDAClient(Client):
    """TD Ameritrade api client"""

    def __init__(self, consumer_key: str, consumer_secret: str):
        """Constructor"""
        super().__init__(consumer_key, consumer_secret)
        self.base_url = "https://api.etrade.com"
        self.session = None
        self._oauth: OAuth2Client = OAuth2Client(  # nosec
            consumer_key,
            #redirect_uri=
        )
        self.request_token, self.request_token_secret = self._oauth.get_request_token(
            params={"oauth_callback": "oob", "format": "json"}
        )
        self.authorize_url, _ = self._oauth.create_authorization_url(
            "https://auth.tdameritrade.com/auth"
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
        self.name = "E*Trade"

    def get_session(self) -> None:
        """Setup the client session."""
        try:
            print("trying to create client")
            self.session = auth.client_from_token_file(self._token_path, self.consumer_key)
        except FileNotFoundError:
            print("token file not found")

    def initialize(self, request) -> None:
        """Initialize the token file."""
        self._token_path = f"env/{str(uuid.uuid4())}.env"
        request_url = request.build_absolute_uri()
        self.client = _create_tda_token(
            self.oauth, request_url, self._api_key, self._token_path
        )
        self._load_accounts()

    def get_accounts(self) -> list[Account]:
        """Get all accounts."""
        parsed_accounts = []
        response = self.session.get_accounts(
            fields=client.Client.Account.Fields.POSITIONS
        )
        # Parse response
        if response is not None and response.status_code == 200:
            data = response.json()
            if (data is not None):
                for account in data:
                    parsed_account = self._parse_account(account["securitiesAccount"])
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
'''
