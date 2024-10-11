# src/immunonaut/pathways/proteins.py
from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias

from .targets import Symbol

class ProteinProtocol(Protocol):
    name: str
    symbol: Symbol

class Proteins:
    ...