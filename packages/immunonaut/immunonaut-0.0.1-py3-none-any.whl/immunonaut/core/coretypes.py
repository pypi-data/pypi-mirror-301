from types import CodeType

import requests
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Type

class CoreType(Enum):
    ENZYME = auto()
    PROTEIN = auto()
    RECEPTOR = auto()
    CELL = auto()
    CYTOKINE = auto()
    PATHWAY = auto()
    SYMBOL = auto()

class TypeRegistry:
    _instance = None
    _registry: Dict[CoreType, Type[Any]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TypeRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, core_type: CoreType, type_class: Type[Any]):
        cls._registry[core_type] = type_class

    @classmethod
    def get(cls, core_type: CoreType) -> Type[Any]:
        return cls._registry.get(core_type)

    @classmethod
    def all_types(cls) -> Dict[CoreType, Type[Any]]:
        return cls._registry.copy()


@dataclass
class UniProtEntity:
    uniprot_id: Optional[str] = None
    name: Optional[str] = None
    sequence: Optional[str] = None
    organism: Optional[str] = None
    function: Optional[str] = None
    subcellular_locations: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    genes: List[str] = field(default_factory=list)

    @classmethod
    def from_uniprot(cls, uniprot_id: str):
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}?format=json"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data for {uniprot_id}")

        data = response.json()

        try:
            name = data['proteinDescription']['recommendedName']['fullName']['value']
        except KeyError:
            name = None

        try:
            genes = [gene['geneName']['value'] for gene in data.get('genes', [])]
        except KeyError as e:
            genes = None

        return cls(
            name=name,
            genes=genes,
            uniprot_id=uniprot_id,
            uniprot_kbid=data["uniProtkbId"],
            sequence=data['sequence']['value'],
            organism=data['organism']['scientificName'],
            function=next((comment['texts'][0]['value'] for comment in data.get('comments', [])
                           if comment['commentType'] == 'FUNCTION'), None),
            subcellular_locations=[location['location']['value'] for location in data.get('subcellularLocations', [])],
            raw_data=data,
        )


@dataclass
class Protein(UniProtEntity):
    molecular_weight: Optional[float] = None
    isoelectric_point: Optional[float] = None

    @classmethod
    def from_uniprot(cls, uniprot_id: str):
        instance = super().from_uniprot(uniprot_id)
        instance.molecular_weight = float(instance.raw_data['sequence']['molWeight']) / 1000  # Convert to kDa
        instance.isoelectric_point = next((feature['description'] for feature in instance.raw_data.get('features', [])
                                           if feature['type'] == 'PI_POINT'), None)
        return instance


@dataclass
class Enzyme(Protein):
    ec_number: Optional[str] = None
    catalytic_activity: Optional[str] = None
    cofactors: List[str] = field(default_factory=list)

    @classmethod
    def from_uniprot(cls, uniprot_id: str):
        instance = super().from_uniprot(uniprot_id)

        for comment in instance.raw_data.get('comments', []):
            if comment['commentType'] == 'CATALYTIC ACTIVITY':
                instance.catalytic_activity = comment['reaction']['name']
            elif comment['commentType'] == 'COFACTOR':
                instance.cofactors = [cofactor['name'] for cofactor in comment.get('cofactors', [])]

        for dbReference in instance.raw_data.get('dbReferences', []):
            if dbReference['type'] == 'EC':
                instance.ec_number = dbReference['id']
                break

        return instance

class Symbol(str):
    pass

# Instantiating the type registry
R = Registrar = TypeRegistry()

# Registration
R.register(CoreType.ENZYME, Enzyme)
R.register(CoreType.PROTEIN, Protein)
R.register(CoreType.SYMBOL, Symbol)