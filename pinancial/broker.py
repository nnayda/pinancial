"""Broker for handling communication."""

from .institution import Insitution
from . import client

class Broker:
    """Handle communciation with an institution."""

    def __init__(
        self,
        key: str,
        secret: str,
        institution: int,
    ):
        """Constructor"""
        self.key = key
        self.secret = secret
        self.institution = institution

        if self.institution == Insitution.TDA:
            self.client = client.TDAClient(key,secret)