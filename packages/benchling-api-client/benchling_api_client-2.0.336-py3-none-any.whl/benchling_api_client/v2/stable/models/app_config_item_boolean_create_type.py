from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemBooleanCreateType(Enums.KnownString):
    BOOLEAN = "boolean"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemBooleanCreateType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppConfigItemBooleanCreateType must be a string (encountered: {val})")
        newcls = Enum("AppConfigItemBooleanCreateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemBooleanCreateType, getattr(newcls, "_UNKNOWN"))
