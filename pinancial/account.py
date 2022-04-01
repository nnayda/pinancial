"""Account model definition."""
from __future__ import annotations
from enum import Enum
from datetime import date


class AccountMode(Enum):
    """Account mode."""

    CASH = "Cash"
    MARGIN = "Margin"


class AccountType(Enum):
    """Account types."""

    AMMCHK = "AMMCHK"
    ARO = "ARO"
    BCHK = "Business Checking"
    BENFIRA = "Beneficiary IRA"
    BENFROTHIRA = "Beneficiary Roth IRA"
    BENF_ESTATE_IRA = "Beneficiary Estate IRA"
    BENF_MINOR_IRA = "Beneficiary Minor IRA"
    BENF_ROTH_ESTATE_IRA = "Beneficiary Roth Estate IRA"
    BENF_ROTH_MINOR_IRA = "Beneficiary Roth Minor IRA"
    BENF_ROTH_TRUST_IRA = "Beneficiary Roth Trust IRA"
    BENF_TRUST_IRA = "Beneficiary Trust IRA"
    BROKER = "Broker"
    CASH = "Cash"
    C_CORP = "C Corp"
    CONTRIBUTORY = "Contributory"
    COVERDELL_ESA = "Coverdell ESA"
    CONVERSION_ROTH_IRA = "Conversion Roth IRA"
    CREDITCARD = "Credit Card"
    COMM_PROP = "Comm Prop"
    CONSERVATOR = "Conservator"
    CORPORATION = "Corporation"
    CSA = "CSA"
    CUSTODIAL = "Custodial"
    DVP = "DVP"
    ESTATE = "Estate"
    EMPCHK = "Employee Checking"
    EMPMMCA = "Employee MMCA"
    ETCHK = "ETCHK"
    ETMMCHK = "ETMMCHK"
    HEIL = "HEIL"
    HELOC = "HELOC"
    INDCHK = "Individual Checking"
    INDIVIDUAL = "Individual"
    INDIVIDUAL_K = "Individual K"
    INVCLUB = "Investment Club"
    INVCLUB_C_CORP = "Investment C Corp"
    INVCLUB_LLC_C_CORP = "Investment Club LLC C Corp"
    INVCLUB_LLC_PARTNERSHIP = "Investment Club LLC Partnership"
    INVCLUB_LLC_S_CORP = "Investment Club LLC S Corp"
    INVCLUB_PARTNERSHIP = "Investment Club Partnership"
    INVCLUB_S_CORP = "Investment Club S Corp"
    INVCLUB_TRUST = "Investment Club Trust"
    IRA_ROLLOVER = "IRA Rollover"
    JOINT = "Joint"
    JTTEN = "JTTEN"
    JTWROS = "JTWROS"
    LLC_C_CORP = "LLC C Corp"
    LLC_PARTNERSHIP = "LLC Partnership"
    LLC_S_CORP = "LLC S Corp"
    LLP = "LLP"
    LLP_C_CORP = "LLP C Corp"
    LLP_S_CORP = "LLP S Corp"
    IRA = "IRA"
    IRACD = "IRACD"
    MONEY_PURCHASE = "Money Purchase"
    MARGIN = "Margin"
    MRCHK = "MRCHK"
    MUTUAL_FUND = "Mutual Fund"
    NONCUSTODIAL = "Non-Custodial"
    NON_PROFIT = "Non-Profit"
    OTHER = "Other"
    PARTNER = "Partner"
    PARTNERSHIP = "Partnership"
    PARTNERSHIP_C_CORP = "Partnership C Corp"
    PARTNERSHIP_S_CORP = "Partnership S Corp"
    PDT_ACCOUNT = "PDT Account"
    PM_ACCOUNT = "PM Account"
    PREFCD = "Pref CD"
    PREFIRACD = "Pref IRA CD"
    PROFIT_SHARING = "Profit Sharing"
    PROPRIETARY = "Proprietary"
    REGCD = "Regular CD"
    ROTHIRA = "Roth IRA"
    ROTH_INDIVIDUAL_K = "Roth Individual K"
    ROTH_IRA_MINORS = "Roth IRA Minors"
    SARSEPIRA = "Sarsep IRA"
    S_CORP = "S Corporation"
    SEPIRA = "Sep IRA"
    SIMPLE_IRA = "Simple IRA"
    TIC = "TIC"
    TRD_IRA_MINORS = "TRD IRA Minors"
    TRUST = "Trust"
    VARCD = "Var CD"
    VARIRACD = "Varir CD"


class AccountStatus(Enum):
    """Status of the account."""

    ACTIVE = "Active"
    CLOSED = "Closed"


class Account:
    """Defines account details at a brokerage."""

    def __init__(
        self,
        account_id: str = "",
        account_key: str = "",
        mode: AccountMode = AccountMode.CASH,
        description: str = "",
        name: str = "",
        acct_type: AccountType = AccountType.OTHER,
        status: AccountStatus = AccountStatus.ACTIVE,
        institution: str = "",
        opened_date: date = None,
        closed_date: date = None,
    ):
        """Constructor"""
        self.account_id = account_id
        self.account_key = account_key
        self.mode = mode
        self.description = description
        self.name = name
        self.acct_type = acct_type
        self.status = status
        self.institution = institution
        self.opened_date = opened_date
        self.closed_date = closed_date

    def __str__(self) -> str:
        return f"{self.institution}: {self.name}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> dict:
        """Return details as dict."""
        return vars(self)
