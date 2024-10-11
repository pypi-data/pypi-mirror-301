# src/immunonaut/_protocols.py
from collections import deque
from typing import Any, Dict, Generic, List, Protocol, Set, TypeAlias, TypeVar

# from .cytokines import Cytokines
# from .proteins import Proteins
# from .targets import Receptors

# Custom typing
Signal: TypeAlias = str | List[str]
Stimulus: TypeAlias = str | List[str]
SignalingPathway: TypeAlias = Dict[Signal, Set[Signal]]
T = TypeVar("T")

class Pathway(Protocol):
    stimulus: Signal
    effect: Signal
    target: SignalingPathway
    stack: deque[T]

class SignalStack(Generic[T]):
    def __init__(self):
        self.stack: deque[T] = deque()

    def push(self, item: T) -> None:
        self.stack.append(item)

    def pop(self, item: T) -> T:
        return self.stack.pop()

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def peek(self) -> bool:
        return self.stack[-1] if self.stack else None

class AntigenProtocol(Protocol):
    effect: SignalingPathway


