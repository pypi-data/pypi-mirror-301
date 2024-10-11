from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, TypeAlias, Tuple, Union

# Custom typing
Abundance: TypeAlias = Union[int, float, Tuple[Union[int, float], Union[int, float]]]
Role: TypeAlias = str
AntigenPresentingCell: TypeAlias = Role
APC: TypeAlias = AntigenPresentingCell
Phagocyte: TypeAlias = Role

# Protocols
class CellType(Protocol):
    name: str | None = "unidentified"
    role: Optional[Role | List[Role] | None] = None
    abundance: Abundance = 0

# Innate immune system
class Monocyte(CellType):
    name = "monocyte"
    role: AntigenPresentingCell | Phagocyte
    abundance: Abundance

    class Macrophage(CellType):
        name = "macrophage"
        role: AntigenPresentingCell | Phagocyte
        abundance: Abundance

    class Dendritic(CellType):
        name = "dendritic"
        role: AntigenPresentingCell | Phagocyte
        abundance: Abundance

class Granulocyte(CellType):
    name = "granulocytes"
    role: AntigenPresentingCell | Phagocyte
    abundance: Abundance

    class Basophil(CellType):
        name = "basophil"
        role: Role = Phagocyte
        abundance: Abundance

    class Eosinophil(CellType):
        name = "eosinophil"
        role: Role = Phagocyte
        abundance: Abundance

    class Neutrophil(CellType):
        name = "neutrophil"
        role: Role = Phagocyte
        abundance: Abundance

# Adaptive immune system
class Lymphocyte(CellType):
    name = "lymphocyte"
    role: Role | List[Role] = "adaptive_immunity"
    abundance: Abundance

    # T Cells
    class T(CellType):
        name = "T"
        role: Role | List[Role] = "adaptive_immunity"
        abundance: Abundance

        class Helper(CellType):
            name = "helper"
            role: Role | List[Role] = "adaptive_immunity"
            abundance: Abundance

        class Killer(CellType):
            name = "killer"
            role: Role | List[Role] = "adaptive_immunity"
            abundance: Abundance

    # B Cells
    class B(CellType):
        name = "B"
        role: Role | List[Role] = "adaptive_immunity"
        abundance: Abundance

        class Effector(CellType):
            name = "effector"
            role: Role | List[Role] = "adaptive_immunity"
            abundance: Abundance

        class Memory(CellType):
            name = "memory"
            role: Role | List[Role] = "adaptive_immunity"
            abundance: Abundance