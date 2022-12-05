"""Base class for api client"""
from __future__ import annotations

from authlib.integrations.httpx_client import OAuth2Client

from pinancial.account import Account

class Client():
    """API client."""
    _oauth_client = OAuth2Client
    auth_endpoint = ""
    token_endpoint = ""
    accounts_endpoint = ""

    def __init__(self, key: str, secret: str, redirect_url: str = ""):
        """Constructor."""
        self.key = key
        self.secret = secret
        self.redirect_url = redirect_url
        self.oauth = self._oauth_client(key,redirect_uri=redirect_url)

    def get_authorization_url(self) -> str:
        """Retrieve authorization url."""
        url, state = self.oauth.create_authorization_url(
            url=self.auth_endpoint,
            redirect_uri=self.redirect_url,
            response_type="code",
        )
        return url

    def get_session(self, response_url: str) -> None:
        """Get an authorized session."""
        self.token = self.oauth.fetch_token(
            self.token_endpoint,
            authorization_response=response_url,
            access_type='offline',
            client_id=self.key,
            include_client_id=True,
        )
        self.oauth = self._oauth_client(
            self.key,
            token=self.token,
            auto_refresh_url=self.token_endpoint,
            auto_refresh_kwargs={'client_id': self.key},
        )

    def load_session(self, token: dict) -> None:
        """Load a previous session."""
        self.token = token
        self.oauth = self._oauth_client(
            self.key,
            token=token,
            auto_refresh_url=self.token_endpoint,
            auto_refresh_kwargs={'client_id': self.key},
        )
        
    def fetch_accounts(self) -> list[Account]:
        """Get the accounts for a client."""
        accounts = []
        response = self.oauth.get(
            self.accounts_endpoint,
            params={"fields":"positions,orders"},
        )
        if response.status_code == 200:
            for record in response.json():
                acct = self.parse_account(record)
                acct.balance = self.parse_balance(record)
                acct.positions = self.parse_positions(record)
                accounts.append(acct)
        return accounts

    def parse_account(self, record: dict) -> Account:
        """Parse an account record from a json response."""

