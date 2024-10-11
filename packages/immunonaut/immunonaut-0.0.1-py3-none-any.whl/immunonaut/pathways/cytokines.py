# src/immunonaut/pathways/cytokines.py
from collections import deque
from dataclasses import dataclass
from typing import List, Protocol
from immunonaut.pathways.human_pathways import HumanPathways
from immunonaut.pathways._protocols import Pathway, SignalingPathway

@dataclass
class Cytokine(Protocol):
    symbol: str
    pathways: deque[Pathway]

@dataclass
class Cytokines:

    @dataclass
    class Interleukins:

        @dataclass
        class IL_6(Cytokine):
            symbol: "IL-6"
            pathways: deque[SignalingPathway] = deque([
                HumanPathways.ComplementPathways.ClassicalPathway,
                HumanPathways.ComplementPathways.AlternativePathway,
                HumanPathways.ComplementPathways.LectinPathway
            ])

        @dataclass
        class IL_8(Cytokine):
            symbol: "IL-8"
            pathways: deque[SignalingPathway] = deque([
                HumanPathways.ComplementPathways.ClassicalPathway,
                HumanPathways.ComplementPathways.AlternativePathway,
                HumanPathways.ComplementPathways.LectinPathway
            ])

