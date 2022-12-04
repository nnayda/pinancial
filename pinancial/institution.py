"""Available financial institutions"""
from __future__ import annotations
from aenum import Enum


class Insitution(Enum):
    """Financial institution."""

    _init_ = 'value string'

    TDA = 1, "TD Ameritrade"
    ETRADE = 2, "E*Trade"

    def __str__(self):
        return self.string

