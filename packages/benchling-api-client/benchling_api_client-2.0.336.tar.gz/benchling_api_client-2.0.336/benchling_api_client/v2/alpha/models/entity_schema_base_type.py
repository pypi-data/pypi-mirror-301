from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntitySchemaBaseType(Enums.KnownString):
    CUSTOM_ENTITY = "custom_entity"
    DNA_SEQUENCE = "dna_sequence"
    RNA_SEQUENCE = "rna_sequence"
    AA_SEQUENCE = "aa_sequence"
    MIXTURE = "mixture"
    DNA_OLIGO = "dna_oligo"
    RNA_OLIGO = "rna_oligo"
    MOLECULE = "molecule"
    ENTRY = "entry"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntitySchemaBaseType":
        if not isinstance(val, str):
            raise ValueError(f"Value of EntitySchemaBaseType must be a string (encountered: {val})")
        newcls = Enum("EntitySchemaBaseType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntitySchemaBaseType, getattr(newcls, "_UNKNOWN"))
