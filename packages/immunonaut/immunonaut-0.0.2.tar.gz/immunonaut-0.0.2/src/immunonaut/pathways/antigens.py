# src/immunonaut/pathways/antigens.py
from typing import Any, List, TypeAlias

from ._protocols import AntigenProtocol
from immunonaut.pathways.human_pathways import HumanPathways
from immunonaut.pathways._protocols import SignalingPathway

class Antigen(AntigenProtocol):
    name: str | None = None
    target: Any[SignalingPathway] | None = None

class Antigens(Antigen):

    class Bacteria(Antigen):
        name: str = "unspecified bacterium"
        target: SignalingPathway | None = None

        class MRSA(Antigen):
            name: str = "methicillin-resistant staphylococcus aureus"
            target: SignalingPathway | None = [
                HumanPathways.ComplementPathways.AlternativePathway,
                HumanPathways.ComplementPathways.ClassicalPathway,
                HumanPathways.ComplementPathways.LectinPathway,
            ]