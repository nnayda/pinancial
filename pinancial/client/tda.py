"""Client for TD Ameritrade API"""
from __future__ import annotations

from pinancial.account import Account
from pinancial.balance import Balance
from pinancial.client.base import Client
from pinancial.instrument import Instrument,InstrumentType
from pinancial.position import Position

def normalize_api_key(api_key):
    api_key_suffix = '@AMER.OAUTHAP'

    if not api_key.endswith(api_key_suffix):
        key_split = api_key.split('@')
        if len(key_split) != 1:
            api_key = key_split[0]

        api_key = api_key + api_key_suffix

    return api_key

class TDAClient(Client):
    """API client for TD Ameritrade."""
    
    auth_endpoint = "https://auth.tdameritrade.com/auth"
    token_endpoint = "https://api.tdameritrade.com/v1/oauth2/token"
    accounts_endpoint = "https://api.tdameritrade.com/v1/accounts"
    
    def __init__(self, key: str, secret: str, redirect_url: str = ""):
        """Constructor."""
        super().__init__(
            normalize_api_key(key),
            secret,
            redirect_url,
        )

    def parse_account(self, record: dict) -> Account|None:
        """Parse an account record from a json response."""
        if "securitiesAccount" in record:
            return Account(
                account_id=record["securitiesAccount"].get("accountId"),
                broker=self,
                acct_type=record["securitiesAccount"].get("type",""),
                is_day_trader=record["securitiesAccount"].get("isDayTrader",False),
                is_closing_only_restricted=record["securitiesAccount"].get("isClosingOnlyRestricted",False),
            )
        return None

    def parse_balance(self, record: dict) -> Balance|None:
        """Parse a balance record from a json response."""
        if "securitiesAccount" in record:
            if "initialBalances" in record["securitiesAccount"]:
                return Balance(
                    accrued_interest=record["securitiesAccount"]["initialBalances"].get("accruedInterest",0.0),
                    cash=record["securitiesAccount"]["initialBalances"].get("cashAvailableForWithdrawal",0.0),
                    long_option_value=record["securitiesAccount"]["initialBalances"].get("longOptionMarketValue",0.0),
                    market_value=record["securitiesAccount"]["initialBalances"].get("liquidationValue",0.0),
                    long_market_value=record["securitiesAccount"]["initialBalances"].get("longMarketValue",0.0),
                    short_market_value=record["securitiesAccount"]["initialBalances"].get("shortMarketValue",0.0),
                    pending_deposits=record["securitiesAccount"]["initialBalances"].get("pendingDeposits",0.0),
                    short_option_value=record["securitiesAccount"]["initialBalances"].get("shortOptionMarketValue",0.0),
                    unsettled_cash=record["securitiesAccount"]["initialBalances"].get("unsettledCash",0.0),
                )
        return None

    def parse_positions(self, record: dict) -> list[Position]:
        """Parse a position record from json response."""
        positions = []
        if "securitiesAccount" in record:
            if "positions" in record["securitiesAccount"]:
                for entry in record["securitiesAccount"]["positions"]:
                    instrument = self.parse_instrument(entry)
                    positions.append(
                        Position(
                            quantity=(
                                entry.get("shortQuantity",0.0) * -1
                                + entry.get("longQuantity",0.0)
                            ),
                            average_price=entry.get("averagePrice",0.0),
                            pl=entry.get("currentDayProfitLoss",0.0),
                            pl_pct=entry.get("currentDayProfitLossPercentage",0.0),
                            market_value=entry.get("marketValue",0.0),
                            instrument=instrument,
                        )
                    )
        return positions

    def parse_instrument(self, record: dict) -> Instrument|None:
        """Parse an instrument record from json response."""
        instrument_map = {
            "NONE": None,
            "EQUITY": InstrumentType.EQUITY,
            "CASH_EQUIVALENT": InstrumentType.CASH,
        }
        if "instrument" in record:
            return Instrument(
                type=instrument_map[record["instrument"].get("assetType","NONE")],
                cusip=record["instrument"].get("cusip",""),
                symbol=record["instrument"].get("symbol",""),
            )
        return None

