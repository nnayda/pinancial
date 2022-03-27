"""Utility functions used throughout."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml


def key_found(data: dict, *args: list) -> bool:
    """Ensures all keys are found in a dictionary."""
    if len(args) == 1:
        return args[0] in data
    if args[0] in data:
        return key_found(data[args[0]], *args[1:])
    return False


def get_item(data: dict, *args: list) -> Any:
    """Get an item from a dict based on a list of keys."""
    if len(args) == 1:
        return data[args[0]]
    return get_item(data[args[0]], *args[1:])


def get_settings(filename: Path) -> dict:
    """Load settings from a yaml file."""
    with open(filename, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return {}
