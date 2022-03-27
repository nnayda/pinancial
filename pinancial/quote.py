"""Define quote details for a given instrument."""
from __future__ import annotations
from datetime import date, datetime
from enum import Enum
from typing import Any
from .instrument import Instrument


class Quote:
    """Abstract quote definition."""

    def __init__(
        self,
        instrument: Instrument,
        change: float = 0,
        change_percent: float = 0,
        previous_close: float = 0,
        last_trade_time: datetime = None,
        low_date: date = None,
        high_date: date = None,
        high52: float = 0,
        low52: float = 0,
        last_trade: float = 0,
        exchange_code: str = "",
    ):
        """Constructor."""
        # Instrument the quote is for
        self.instrument = instrument
        # Dollar change of the last price from the previous close
        self.change = change
        # Official price at the close of the previous trading day
        self.previous_close = previous_close
        # Percentage change of the last price from the previous close
        self.change_percent = change_percent
        # The time when the last trade was placed
        self.last_trade_time = last_trade_time
        # The date at which the price was the lowest in the last 52 weeks; applicable for stocks
        # and mutual funds
        self.low_date = low_date
        # The date at which the price was highest in the last 52 weeks; applicable for stocks and
        # mutual funds
        self.high_date = high_date
        # Highest price at which a security has traded during the past year (52 weeks).
        # For options, this value is the lifetime high.
        self.high52 = high52
        # Lowest price at which security has traded during the past year (52 weeks). For options,
        # this value is the lifetime low.
        self.low52 = low52
        # Price of the most recent trade of a security
        self.last_trade = last_trade
        # Exchange code of the primary listing exchange for this instrument
        self.exchange_code = exchange_code


class EquityQuote(Quote):
    """Quote details for an equity."""

    def __init__(
        self,
        ask: float = 0,
        ask_size: int = 0,
        ask_time: datetime = None,
        bid: float = 0,
        bid_exchange: str = "",
        bid_size: int = 0,
        bid_time: datetime = None,
        direction: int = 0,
        dividend: float = 0,
        eps: float = 0,
        earnings: float = 0,
        exdividend_date: date = None,
        high: float = 0,
        low: float = 0,
        open_price: float = 0,
        open_interest: int = 0,
        previous_volume: int = 0,
        volume: int = 0,
        cash_deliverable: float = 0,
        market_cap: float = 0,
        shares_outstanding: float = 0,
        earnings_date: date = None,
        beta: float = 0,
        dividend_yield: float = 0,
        declared_dividend: float = 0,
        dividend_payable_date: date = None,
        price_earnings: float = 0,
        avg_volume: int = 0,
        **kwargs: Any,
    ):
        """Constructor."""
        super().__init__(**kwargs)
        # The current ask price for a security
        self.ask = ask
        # Number shares or contracts offered by broker or dealer at the ask price
        self.ask_size = ask_size
        # The time of the ask; for example, '15:15:43 PDT 03-21-2018'
        self.ask_time = ask_time
        # Current bid price for a security
        self.bid = bid
        # Code for the exchange reporting the bid price
        self.bid_exchange = bid_exchange
        # Number of shares or contracts offered at the bid price
        self.bid_size = bid_size
        # Time of the bid; for example '15:15:43 PDT 03-21-2018'
        self.bid_time = bid_time
        # Direction of movement; that is, whether the current price is higher or lower than the
        # price of the most recent trade
        self.direction = direction
        # Cash amount per share of the latest dividend
        self.dividend = dividend
        # Earnings per share on rolling basis (stocks only)
        self.eps = eps
        # Projected Earnings per share for the next fiscal year (stocks only)
        self.earnings = earnings
        # Date (in Epoch time) on which shareholders were entitled to receive the latest dividend
        self.exdividend_date = exdividend_date
        # Highest price at which a security has traded during the current day
        self.high = high
        # Lowest price at which a security has traded during the current day
        self.low = low
        # Price of a security at the current day's market open
        self.open_price = open_price
        # Total number of options or futures contracts that are not closed or delivered on a
        # particular day
        self.open_interest = open_interest
        # Final volume from the previous market session
        self.previous_volume = previous_volume
        # Total number of shares or contracts exchanging hands
        self.volume = volume
        # The cash deliverables in case of multiple deliverables
        self.cash_deliverable = cash_deliverable
        # The value market capitalization
        self.market_cap = market_cap
        # The number of outstanding shares
        self.shares_outstanding = shares_outstanding
        # the next earning date
        self.earnings_date = earnings_date
        # A measure of a stock's volatility relative to the primary market index
        self.beta = beta
        # The dividend yield
        self.dividend_yield = dividend_yield
        # The declared dividend
        self.declared_dividend = declared_dividend
        # The dividend payable date
        self.dividend_payable_date = dividend_payable_date
        # The price to earnings
        self.price_earnings = price_earnings
        # Average volume value corresponding to the symbol
        self.avg_volume = avg_volume


class OptionDeliverable:
    """Defines option deliverable details."""

    def __init__(
        self,
        root_symbol: str = "",
        symbol: str = "",
        type_code: str = "",
        exchange_code: str = "",
        strike_percent: float = 0,
        cil_shares: float = 0,
        whole_shares: int = 0,
    ):
        """Constructor."""
        # Root symbol of option multiplier
        self.root_symbol = root_symbol
        # Symbol of share to be delivered
        self.symbol = symbol
        # Type code of share to be delivered
        self.type_code = type_code
        # Exchange code of share to be delivered
        self.exchange_code = exchange_code
        # Strike percent of delivered product
        self.strike_percent = strike_percent
        # Number of CIL shares to be delivered
        self.cil_shares = cil_shares
        # Number of whole shares to be distributed
        self.whole_shares = whole_shares


class OptionStyle(Enum):
    """Available option sytles."""

    # options can be exercised only on the expiration date
    EUROPEAN = "European"
    # options can be exercised any time before they expire
    AMERICAN = "American"
    UNKNOWN = "Unknown"


class OptionType(Enum):
    """Available option typse."""

    CALL = "Call"
    PUT = "Put"
    OTHER = "Other"


class OptionQuote(EquityQuote):
    """Quote details for an option."""

    def __init__(
        self,
        option_type: OptionType = OptionType.OTHER,
        strike_price: float = 0,
        option_multiplier: float = 0,
        contract_size: float = 0,
        expiration_date: date = None,
        option_previous_bid_price: float = 0,
        option_previous_ask_price: float = 0,
        intrinsic_value: float = 0,
        time_premium: float = 0,
        days_to_expiration: int = 0,
        option_deliverables: list[OptionDeliverable] = None,
        option_style: OptionStyle = OptionStyle.UNKNOWN,
        option_underlier: str = "",
        option_underlier_exchange: str = "",
        osi_key: str = "",
        **kwargs: Any,
    ):
        """Constructor."""
        super().__init__(**kwargs)
        # The option type - either CALL or PUT
        self.option_type = option_type
        # The strike price for the option
        self.strike_price = strike_price
        # The option multiplier value
        self.option_multiplier = option_multiplier
        # The contract size of the option
        self.contract_size = contract_size
        # The expiration date of the option
        self.expiration_date = expiration_date
        # The option previous bid price
        self.option_previous_bid_price = option_previous_bid_price
        # The option previous ask price
        self.option_previous_ask_price = option_previous_ask_price
        # The intrinsic value of the share
        self.intrinsic_value = intrinsic_value
        # The value of the time premium
        self.time_premium = time_premium
        # Number of days before the option expires
        self.days_to_expiration = days_to_expiration
        # List of mulitple deliverables
        self.option_deliverables = option_deliverables
        # Specifies how the contract treats the expiration date.
        self.option_style = option_style
        # Symbol for the underlier (options only)
        self.option_underlier = option_underlier
        # Exchange code for option underlier symbol; applicable only for options
        self.option_underlier_exchange = option_underlier_exchange
        # The Options Symbology Initiative (OSI) representation of the option symbol
        self.osi_key = osi_key


class SalesCharge:
    """Stores sales charge details for mutual funds."""

    def __init__(
        self,
        low_high: str = "",
        percent: str = "",
    ):
        """Constructor."""
        # The sales charge for investing in the mutual fund expressed as a low-high range
        # (usually the sales charge is between 3-6%)
        self.low_high = low_high
        # The percentage of the investment spent on the sales charge
        self.percent = percent


class MutualFundQuote(Quote):
    """Mutual Fund object."""

    def __init__(
        self,
        cusip: str = "",
        transaction_fee: bool = False,
        early_redemption_fee: str = "",
        availability: bool = False,
        initial_investment: float = 0,
        subsequent_investment: float = 0,
        fund_family: str = "",
        net_value: float = 0,
        public_offer_price: float = 0,
        net_expense_ratio: float = 0,
        gross_expense_ratio: float = 0,
        order_cutoff_time: datetime = None,
        sales_charge: str = "",
        initial_ira_investment: float = 0,
        subsequent_ira_investment: float = 0,
        net_assets: float = 0,
        inception_date: date = None,
        avg_annual_return: float = 0,
        seven_day_curr_yield: float = 0,
        annual_total_return: float = 0,
        weighted_avg_maturity: float = 0,
        avg_annual_return_1yr: float = 0,
        avg_annual_return_3yr: float = 0,
        avg_annual_return_5yr: float = 0,
        avg_annual_return_10yr: float = 0,
        exchange_name: str = "",
        since_inception: float = 0,
        quarterly_since_inception: float = 0,
        actual_12b1_fee: float = 0,
        performance_asof_date: date = None,
        quarterly_performance_asof_date: date = None,
        morning_start_cat: str = "",
        monthly_trailing_return_ytd: float = 0,
        monthly_trailing_return_1m: float = 0,
        monthly_trailing_return_3m: float = 0,
        monthly_trailing_return_6m: float = 0,
        monthly_trailing_return_1y: float = 0,
        monthly_trailing_return_3y: float = 0,
        monthly_trailing_return_5y: float = 0,
        monthly_trailing_return_10y: float = 0,
        quarterly_trailing_return_ytd: float = 0,
        quarterly_trailing_return_1m: float = 0,
        quarterly_trailing_return_3m: float = 0,
        quarterly_trailing_return_6m: float = 0,
        etrade_early_redemption_fee: str = "",
        max_sales_load: float = 0,
        deferred_sales_charges: list[SalesCharge] = None,
        frontend_sales_charges: list[SalesCharge] = None,
        **kwargs: Any,
    ):
        """Constructor."""
        super().__init__(**kwargs)
        # The identifier for the security
        self.cusip = cusip
        # An indicator (yes or no) whether or not there is a fee applicable for the security
        # transaction
        self.transaction_fee = transaction_fee
        # The redemption fee applicable for the security transaction
        self.early_redemption_fee = early_redemption_fee
        # An indicator to inform if the mutual fund is available for new buy and sell orders
        self.availability = availability
        # The minimum initial investment required to purchase the fund
        self.initial_investment = initial_investment
        # The minimum subsequent investment amount
        self.subsequent_investment = subsequent_investment
        # The type of fund family the mutual fund belongs to
        self.fund_family = fund_family
        # The Net Access Value (NAV) is the fund's per share market value; that is, the bid price
        # investors pay to purchase fund shares
        self.net_value = net_value
        # The Public Offering Price (POP) is the price at which shares are sold to public; for
        # funds without sales commission (that is, load), POP is equal to NAV
        self.public_offer_price = public_offer_price
        # The expense ratio of the fund after application of expense waivers and reimbursements
        self.net_expense_ratio = net_expense_ratio
        # The fund's total annual operating expense ratio gross of any fee waivers or expense
        # reimbursements
        self.gross_expense_ratio = gross_expense_ratio
        # The cut-off time for the purchase and redemption of mutual fund shares
        self.order_cutoff_time = order_cutoff_time
        # The sales charge for the purchase and redemption of mutual fund shares
        self.sales_charge = sales_charge
        # The initial amount needed to purchase mutual fund shares in an IRA account
        self.initial_ira_investment = initial_ira_investment
        # The minimum amount needed to purchase subsequent mutual fund shares in an IRA account
        self.subsequent_ira_investment = subsequent_ira_investment
        # The Total Net Asset Value (NAV)
        self.net_assets = net_assets
        # The date when the fund started
        self.inception_date = inception_date
        # The average annual return at the end of the quarter; this is available if fund has
        # been active for more than 10 years
        self.avg_annual_return = avg_annual_return
        # The seven-day current yield
        self.seven_day_curr_yield = seven_day_curr_yield
        # The annual total return
        self.annual_total_return = annual_total_return
        # The weighted average of maturity
        self.weighted_avg_maturity = weighted_avg_maturity
        # The average annual return for one year
        self.avg_annual_return_1yr = avg_annual_return_1yr
        # The average annual return for three years
        self.avg_annual_return_3yr = avg_annual_return_3yr
        # The average annual return for five years
        self.avg_annual_return_5yr = avg_annual_return_5yr
        # The average annual return for ten years
        self.avg_annual_return_10yr = avg_annual_return_10yr
        # The exchange name of the fund
        self.exchange_name = exchange_name
        # The value of the fund since its beginning
        self.since_inception = since_inception
        # The quarterly average value of the fund since the beginning of fund
        self.quarterly_since_inception = quarterly_since_inception
        # The annual marketing or distribution fee on the mutual fund
        self.actual_12b1_fee = actual_12b1_fee
        # The start date the performance is measured from
        self.performance_asof_date = performance_asof_date
        # The start date of the quarter that the performance is measured from
        self.quarterly_performance_asof_date = quarterly_performance_asof_date
        # NEED TO UPDATE: redemption  Redemption  The mutual fund shares redemption properties
        # The Morningstar category for the fund
        self.morning_start_cat = morning_start_cat
        # The one-year monthly trailing return value
        self.monthly_trailing_return_1y = monthly_trailing_return_1y
        # The three-year monthly trailing return value
        self.monthly_trailing_return_3y = monthly_trailing_return_3y
        # The five-year monthly trailing return value
        self.monthly_trailing_return_5y = monthly_trailing_return_5y
        # The ten-year monthly trailing return value
        self.monthly_trailing_return_10y = monthly_trailing_return_10y
        # The E*TRADE early redemption fee
        self.etrade_early_redemption_fee = etrade_early_redemption_fee
        # The maximum sales charge
        self.max_sales_load = max_sales_load
        # The year-to-date monthly trailing return value
        self.monthly_trailing_return_ytd = monthly_trailing_return_ytd
        # The one-month monthly trailing return value
        self.monthly_trailing_return_1m = monthly_trailing_return_1m
        # The three-month monthly trailing return value
        self.monthly_trailing_return_3m = monthly_trailing_return_3m
        # The six-month monthly trailing return value
        self.monthly_trailing_return_6m = monthly_trailing_return_6m
        # The year-to-date quarterly trailing return value
        self.quarterly_trailing_return_ytd = quarterly_trailing_return_ytd
        # The one-month quarterly trailing return value
        self.quarterly_trailing_return_1m = quarterly_trailing_return_1m
        # The three-month quarterly trailing return value
        self.quarterly_trailing_return_3m = quarterly_trailing_return_3m
        # The six-month quarterly trailing return value
        self.quarterly_trailing_return_6m = quarterly_trailing_return_6m
        # The deferred sales charge
        self.deferred_sales_charges = deferred_sales_charges
        # The front-end sales charge
        self.frontend_sales_charges = frontend_sales_charges
