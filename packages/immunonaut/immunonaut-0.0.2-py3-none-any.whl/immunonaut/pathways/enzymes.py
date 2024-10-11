# src/immunonaut/pathways/enzymes.py
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Any, List, Optional, Protocol, TypeAlias

from .proteins import Proteins
from ._protocols import Signal, SignalingPathway
from .targets import Symbol, Receptors

class EnzymeType(Enum):
    UNSPECIFIED = auto()
    KINASE = auto()
    IRAK = auto()
    MAP3K = auto()

class EnzymeProtocol(Protocol):
    name: str | None
    symbol: Optional[Symbol]
    enzyme_type: Optional[EnzymeType]
    targets: Optional[List["Enzyme"]]

@dataclass
class Enzyme(EnzymeProtocol):
    name: str | None = "unspecified enzyme"
    symbol: Symbol | None = None
    enzyme_type: EnzymeType.UNSPECIFIED
    targets: List["Enzyme"] | None = field(default_factory=list)

class EnzymeRegistry:
    def __init__(self):
        self.enzymes: dict[Symbol, Enzyme] = {}

    def register(self, enzyme: Enzyme):
        if enzyme.symbol:
            self.enzymes[enzyme.symbol] = enzyme

    def get(self, symbol: Symbol) -> Optional[Enzyme]:
        return self.enzymes.get(symbol)

@dataclass
class EnzymeDefinitions:
    registry: EnzymeRegistry = field(default_factory=EnzymeRegistry)

    def __post_init__(self) -> None:
        self.define_enzymes()

    def define_enzymes(self) -> None:
        """
        Encapsulates enzyme definitions.

        :return: EnzymeDefinitions
        """

        # Interleukin-1 Receptor-Associated Kinases
        irak1 = Enzyme(
            name="Interleukin-1 Receptor Associated Kinase 1",
            symbol="IRAK1",
            enzyme_type=EnzymeType.IRAK
        )
        irak2 = Enzyme(
            name="Interleukin-1 Receptor Associated Kinase 2",
            symbol="IRAK2",
            enzyme_type=EnzymeType.IRAK
        )
        irak3 = Enzyme(
            name="Interleukin-1 Receptor Associated Kinase 3",
            symbol="IRAK3",
            enzyme_type=EnzymeType.IRAK
        )
        irak4 = Enzyme(
            name="Interleukin-1 Receptor Associated Kinase 4",
            symbol="IRAK4",
            enzyme_type=EnzymeType.IRAK
        )

        # Mitogen-Activated Protein Kinase Kinase Kinases (MAP3Ks)
        map3k1 = Enzyme(
            name="Mitogen-Activated Protein Kinase Kinase Kinase 1",
            symbol="MAP3K1",
            enzyme_type=EnzymeType.MAP3K
        )
        map3k2 = Enzyme(
            name="Mitogen-Activated Protein Kinase Kinase 2",
            symbol="MAP3K2",
            enzyme_type=EnzymeType.MAP3K
        )
        map3k3 = Enzyme(
            name="Mitogen-Activated Protein Kinase Kinase Kinase 3",
            symbol="MAP3K3",
            enzyme_type=EnzymeType.MAP3K
        )
        map3k4 = Enzyme(
            name="Mitogen-Activated Protein Kinase Kinase Kinase 4",
            symbol="MAP3K4",
            enzyme_type=EnzymeType.MAP3K
        )
        map3k5 = Enzyme(
            name="Mitogen-Activated Protein Kinase Kinase Kinase 5",
            symbol="MAP3K5",
            enzyme_type=EnzymeType.MAP3K
        )
        map3k6 = Enzyme(
            name="Mitogen-Activated Protein Kinase Kinase Kinase 6",
            symbol="MAP3K6",
            enzyme_type=EnzymeType.MAP3K
        )
        map3k7 = Enzyme(
            name="Mitogen-Activated Protein Kinase Kinase Kinase 7",
            symbol="MAP3K7",
            enzyme_type=EnzymeType.MAP3K
        )

        enzymes = [
            irak1, irak2, irak3, irak4,
            map3k1, map3k2, map3k3, map3k4, map3k5, map3k6, map3k7
        ]

        for e in enzymes:
            self.registry.register(e)


def main():
    enzyme_definitions = EnzymeDefinitions()
    return enzyme_definitions.define_enzymes()

if __name__ == "__main__":
    main()