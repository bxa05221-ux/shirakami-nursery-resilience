from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class IndividualSupportPlan(BaseModel):
    child_id: str
    developmental_observation_refs: List[str] = []
    goals: List[str] = Field(min_length=1)
    strengths_and_interests: List[str] = []
    support_policy: List[str] = Field(min_length=1)
    environmental_adjustments: List[str] = []
    participation_and_choice: List[str] = []
    family_collaboration: List[str] = []
    class_integration_notes: List[str] = []
    review_cycle: str = 'monthly'
    status: str = 'draft'
    revision_history: List[str] = []
    approved_by: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class IndividualPlanUpdate(BaseModel):
    goals: Optional[List[str]] = None
    support_policy: Optional[List[str]] = None
    environmental_adjustments: Optional[List[str]] = None
    participation_and_choice: Optional[List[str]] = None
    family_collaboration: Optional[List[str]] = None
    class_integration_notes: Optional[List[str]] = None
    status: Optional[str] = None
    revision_note: str = ''
