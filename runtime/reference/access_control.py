from dataclasses import dataclass
from enum import Enum

class Role(str, Enum):
    STAFF = 'staff'
    CLASS_LEAD = 'class_lead'
    FACILITY_MANAGER = 'facility_manager'
    EXTERNAL_EVALUATOR = 'external_evaluator'
    AI_RUNTIME = 'ai_runtime'

@dataclass(frozen=True)
class AccessContext:
    facility_id: str
    role: Role
    assigned_class_ids: tuple[str, ...] = ()
    can_resolve_identity: bool = False


def identity_visibility(context: AccessContext) -> str:
    if context.role == Role.AI_RUNTIME:
        return 'anonymous_id_only'
    if context.role == Role.EXTERNAL_EVALUATOR:
        return 'anonymized_evidence'
    if context.role == Role.FACILITY_MANAGER and context.can_resolve_identity:
        return 'pseudonym_plus_authorized_resolution'
    if context.role in (Role.STAFF, Role.CLASS_LEAD):
        return 'pseudonym'
    return 'anonymous_id_only'


def can_access_class(context: AccessContext, class_id: str) -> bool:
    if context.role == Role.FACILITY_MANAGER:
        return True
    if context.role == Role.EXTERNAL_EVALUATOR:
        return False
    return class_id in context.assigned_class_ids
