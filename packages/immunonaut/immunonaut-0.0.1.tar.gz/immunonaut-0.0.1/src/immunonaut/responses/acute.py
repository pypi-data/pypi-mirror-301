# src/immunonaut/responses/acute.py
from collections import deque
from typing import Any, List, TypeAlias

from ._protocols import ResponseProtocol
from immunonaut.pathways.antigens import Antigen
from immunonaut.pathways.cytokines import Cytokine, Cytokines
from immunonaut.pathways.targets import Receptors
from immunonaut.pathways._protocols import AntigenProtocol, Signal, SignalingPathway


# Custom typing
Response: TypeAlias = ResponseProtocol | List[ResponseProtocol]

class Responses(ResponseProtocol):

    class Inflammation(ResponseProtocol):
        effectors: Any[Receptors] | Any[Cytokine] | Any[Antigen] = [
            Antigen
        ]
        ligand: Any[Receptors]
        effect: Any[Signal] | Any[SignalingPathway]

    class Suppression(ResponseProtocol):
        effectors: Any[Receptors] | Any[Cytokine]
        ligand: Any[Receptors]
        effect: Any[Signal] | Any[SignalingPathway]