from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class IdentityRecord:
    facility_id: str
    child_id: str
    pseudonym: str
    real_name_reference: str

class IdentityVault:
    """Reference-only identity mapping.

    Production deployment must replace this in-memory implementation with an
    encrypted, facility-controlled store and audited authorization layer.
    The Runtime should normally receive anonymous IDs, not real names.
    """
    def __init__(self):
        self._records: Dict[str, IdentityRecord] = {}

    def register(self, facility_id: str, child_id: str, pseudonym: str, real_name_reference: str) -> None:
        self._records[f'{facility_id}:{child_id}'] = IdentityRecord(
            facility_id=facility_id,
            child_id=child_id,
            pseudonym=pseudonym,
            real_name_reference=real_name_reference,
        )

    def pseudonym(self, facility_id: str, child_id: str) -> Optional[str]:
        record = self._records.get(f'{facility_id}:{child_id}')
        return record.pseudonym if record else None

    def resolve_real_name(self, facility_id: str, child_id: str, authorized: bool = False) -> Optional[str]:
        if not authorized:
            return None
        record = self._records.get(f'{facility_id}:{child_id}')
        return record.real_name_reference if record else None
