# src/immunonaut/models/_protocols.py
from random import uniform
from typing import List, Protocol

from immunonaut.cell_types import (Abundance, CellType, Granulocyte,
                                   Lymphocyte, Monocyte)

# Protocols
class ImmunityProtocol(Protocol):
    abundance_range: Abundance = (0.00, 0.00)
    population: List[CellType] = []

class ImmuneSystem:
    def __init__(
            self,
            cell_count: int = 1000,
            immunocompetent: bool = True
    ) -> None:
        self.cell_count = cell_count
        self.populations = Populations()
        self.granulocytes = self.populations.granulocytes
        self.basophils = self.populations.basophils
        self.eosinophils = self.populations.eosinophils
        self.neutrophils = self.populations.neutrophils
        self.monocytes = self.populations.monocytes
        self.dendritic_cells = self.populations.dendritic_cells
        self.macrophages = self.populations.macrophages
        self.immunocompetent = immunocompetent

        if self.immunocompetent:
            try:
                self.basophils.population = [
                    Granulocyte.Basophil() for _ in range(round(self.basophils.abundance * self.cell_count))
                ]
                self.eosinophils.population = [
                    Granulocyte.Eosinophil() for _ in range(round(self.eosinophils.abundance * self.cell_count))
                ]
                self.neutrophils.population = [
                    Granulocyte.Neutrophil() for _ in range(round(self.neutrophils.abundance * self.cell_count))
                ]
                self.monocytes.population = [
                    Monocyte() for _ in range(round(self.monocytes.abundance * self.cell_count))
                ]
                self.dendritic_cells.population = [
                    Monocyte.Dendritic() for _ in range(round(self.dendritic_cells.abundance * self.cell_count))
                ]
                self.macrophages.population = [
                    Monocyte.Macrophage() for _ in range(round(self.macrophages.abundance * self.cell_count))
                ]
            except ValueError as e:
                print("Improper value passed to some caller in the WBC initialization block: ", e)
            except Exception as e:
                print("Error: ", e)


class Populations:
    def __init__(self):
        self.granulocytes = Granulocytes()
        self.basophils = self.granulocytes.Basophils()
        self.eosinophils = self.granulocytes.Eosinophils()
        self.neutrophils = self.granulocytes.Neutrophils()
        self.monocytes = Monocytes()
        self.dendritic_cells = self.monocytes.DendriticCells()
        self.macrophages = self.monocytes.Macrophages()
        self.lymphocytes = Lymphocytes()
        
# Cell type population objects
class Granulocytes(ImmunityProtocol):
    def __init__(self) -> None:
        self.abundance_range: Abundance = (0.0, 0.0)
        self.abundance: Abundance = uniform(self.abundance_range[0], self.abundance_range[1])
        self.population: [Granulocyte] = []

    class Basophils(ImmunityProtocol):
        def __init__(self) -> None:
            self.abundance_range: Abundance = (0.005, 0.01)
            self.abundance: Abundance = uniform(self.abundance_range[0], self.abundance_range[1])
            self.population: [Granulocyte.Basophil | None] = []

    class Eosinophils(ImmunityProtocol):
        def __init__(self):
            self.abundance_range: Abundance = (0.01, 0.04)
            self.abundance: Abundance = uniform(self.abundance_range[0], self.abundance_range[1])
            population: [Granulocyte.Eosinophil | None] = []

    class Neutrophils(ImmunityProtocol):
        def __init__(self):
            self.abundance_range: Abundance = (0.4, 0.6)
            self.abundance: Abundance = uniform(self.abundance_range[0], self.abundance_range[1])
            self.population: [Granulocyte.Neutrophil | None] = []

class Monocytes(ImmunityProtocol):
    def __init__(self):
        self.abundance_range: Abundance = (0.02, 0.08)
        self.abundance: Abundance = uniform(self.abundance_range[0], self.abundance_range[1])
        self.population: [Monocyte | None] = []

    class DendriticCells(ImmunityProtocol):
        def __init__(self):
            self.abundance_range: Abundance = (0.0, 0.0)
            self.abundance: Abundance = uniform(self.abundance_range[0], self.abundance_range[1])
            self.population: [Monocyte.Dendritic | None] = []

    class Macrophages(ImmunityProtocol):
        def __init__(self):
            self.abundance_range: Abundance = (0.0, 0.0)
            self.abundance: Abundance = uniform(self.abundance_range[0], self.abundance_range[1])
            self.population: [Monocyte.Macrophage | None] = []

class Lymphocytes(ImmunityProtocol):
    def __init__(self):
        self.abundance_range: Abundance = (0.2, 0.4)
        self.abundance: Abundance = uniform(self.abundance_range[0], self.abundance_range[1])
        self.population: [Lymphocyte | None] = []

def main() -> ImmuneSystem:
    immune_system = ImmuneSystem()
    return immune_system

# TODO: Model adaptive immune system.

if __name__ == '__main__':
    main()