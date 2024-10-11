# src/immunonaut/mapping.py
from dataclasses import dataclass, field
from typing import List, TypeAlias

from immunonaut.cell_types import (Granulocyte, Lymphocyte, Monocyte)

from immunonaut.targets import Receptor

# Custom types
Species: TypeAlias = str

@dataclass
class HUMAN:
    species: Species = "human"
    NODs: List[Receptor.NodLikeReceptors.NODs] = field(default_factory=lambda: [
        Receptor.NodLikeReceptors.NODs.NOD1,
        Receptor.NodLikeReceptors.NODs.NOD2,
        Receptor.NodLikeReceptors.NODs.NOD3,
        Receptor.NodLikeReceptors.NODs.NOD4,
        Receptor.NodLikeReceptors.NODs.NOD5
    ]
                                                       )
    NLRPs: List[Receptor.NodLikeReceptors.NLRPs] = field(default_factory=lambda: [
        Receptor.NodLikeReceptors.NLRPs.NLRP1,
        Receptor.NodLikeReceptors.NLRPs.NLRP2,
        Receptor.NodLikeReceptors.NLRPs.NLRP3,
        Receptor.NodLikeReceptors.NLRPs.NLRP4,
        Receptor.NodLikeReceptors.NLRPs.NLRP5,
        Receptor.NodLikeReceptors.NLRPs.NLRP6
    ]
                                                         )
    TLRs: List[Receptor.TollLikeReceptors] = field(default_factory=lambda: [
        Receptor.TollLikeReceptors.TLR1,
        Receptor.TollLikeReceptors.TLR2,
        Receptor.TollLikeReceptors.TLR3,
        Receptor.TollLikeReceptors.TLR4,
        Receptor.TollLikeReceptors.TLR5,
        Receptor.TollLikeReceptors.TLR6,
        Receptor.TollLikeReceptors.TLR7,
        Receptor.TollLikeReceptors.TLR8,
        Receptor.TollLikeReceptors.TLR9,
        Receptor.TollLikeReceptors.TLR10,
        Receptor.TollLikeReceptors.TLR11,
        Receptor.TollLikeReceptors.TLR12,
        Receptor.TollLikeReceptors.TLR13,
        Receptor.TollLikeReceptors.TLR14
        ]
                                                   )

    CELL_TYPES = (
        Granulocyte.Basophil,
        Monocyte.Dendritic,
        Granulocyte.Eosinophil,
        Monocyte.Macrophage,
        Monocyte,
        Granulocyte.Neutrophil,
        Lymphocyte,
        Lymphocyte.T,
        Lymphocyte.B,
        Lymphocyte.T.Helper,
        Lymphocyte.T.Killer,
        Lymphocyte.B.Effector,
        Lymphocyte.B.Memory
    )