# src/immunonaut/pathways/main.py
from collections import deque
from typing import Callable, List, Optional, Set

from ._protocols import (
    Pathway, Signal, SignalingPathway,
    SignalStack, Stimulus, T
)
from .human_pathways import PATHWAYS

class PathwayManager:
    def __init__(self, pathway: SignalingPathway):
        self.pathway = pathway

    def add_signal(self, signal: Signal, next_signals: Optional[List[Signal]] = None) -> None:
        if signal not in self.pathway:
            self.pathway[sign`al] = set()
        if next_signals:
            self.pathway[signal].update(next_signals)

    def get_next_signals(self, signal: Signal) -> Set[Signal]:
        return self.pathway.get(signal, set())

    def all_signals(self) -> Set[Signal]:
        return set(self.pathway.keys())

class PathwayTraverser:
    def __init__(self, pathway_manager: PathwayManager):
        self.pathway_manager = pathway_manager
        self.traversal_stack = deque()

    def dfs_traverse(self, start_signal: Signal, process_func: Callable[[Signal], None]) -> None:
        visited = set()
        self.traversal_stack.clear()
        self.traversal_stack.append(start_signal)

        while self.traversal_stack:
            current_signal = self.traversal_stack.pop()
            if current_signal not in visited:
                visited.add(current_signal)
                process_func(current_signal)

                for next_signal in self.pathway_manager.get_next_signals(current_signal):
                    if next_signal not in visited:
                        self.traversal_stack.append(next_signal)

    def reset_traversal(self) -> None:
        self.traversal_stack.clear()

def main():
    pathway: SignalingPathway = {}
    pathway_manager = PathwayManager(pathway)
    traverser = PathwayTraverser(pathway_manager)
    return pathway, pathway_manager, traverser

if __name__ == '__main__':
    main()
