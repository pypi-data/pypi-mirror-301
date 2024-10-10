from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2WorkflowTaskUpdatedAssigneeEventEventType(Enums.KnownString):
    V2_WORKFLOWTASKUPDATEDASSIGNEE = "v2.workflowTask.updated.assignee"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2WorkflowTaskUpdatedAssigneeEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2WorkflowTaskUpdatedAssigneeEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2WorkflowTaskUpdatedAssigneeEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2WorkflowTaskUpdatedAssigneeEventEventType, getattr(newcls, "_UNKNOWN"))
