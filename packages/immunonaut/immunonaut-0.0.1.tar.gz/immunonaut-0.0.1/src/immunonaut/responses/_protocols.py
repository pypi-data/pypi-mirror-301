# src/immunonaut/respopnses/_protocols.py
from typing import Any, Protocol, TypeAlias

from immunonaut.pathways.cytokines import Cytokine
from immunonaut.pathways._protocols import Signal, Pathway, SignalingPathway
from immunonaut.pathways.targets import Receptors
from immunonaut.responses.acute import Responses

class ResponseProtocol(Protocol):
    effector: Any[Cytokine] | Any[Receptors] | Any[Signal] | Any[SignalingPathway]
    ligand: Any[Receptors]
    target: Any[Receptors] | Any[Cytokine] | Any[Signal] | Any[SignalingPathway]
    effect: Any[Responses.Inflammation] | Any[Responses.Suppression]
