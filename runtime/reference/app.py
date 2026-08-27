from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from facility_landscape import build_facility_landscape
from presence_time import build_presence_time_landscape
from external_landscape import build_external_landscape

app = FastAPI(title='Shirakami Nursery Resilience API', version='0.1.0-alpha1')

class Observation(BaseModel):
    class_id: str
    facts: List[str] = Field(min_length=1)
    child_id: Optional[str] = None
    child_voice_or_choice: Optional[str] = None
    observed_at: datetime = Field(default_factory=datetime.utcnow)

class Landscape(BaseModel):
    class_id: str
    attendance: int = Field(ge=0, le=20)
    assigned_staff: int = Field(ge=0)
    note: Optional[str] = None

class SafetySignal(BaseModel):
    signal_type: str
    facts: List[str] = Field(min_length=1)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

class ExternalSignal(BaseModel):
    category: str
    source: str
    observed_at: datetime = Field(default_factory=datetime.utcnow)
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    area: Optional[str] = None
    severity: str = 'info'
    summary: str
    source_url: Optional[str] = None
    raw_reference: Optional[str] = None

class ChildPresence(BaseModel):
    facility_id: str
    child_id: str
    class_id: str
    date: str
    scheduled_arrival: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    scheduled_departure: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    status: str = 'scheduled'
    attendance_note: Optional[str] = None
    recorded_by: str

class StaffPresence(BaseModel):
    facility_id: str
    staff_id: str
    date: str
    scheduled_start: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    break_minutes: int = Field(default=0, ge=0)
    assigned_class_ids: List[str] = []
    recorded_by: str

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

observations: List[Observation] = []
landscapes: List[Landscape] = []
safety_signals: List[SafetySignal] = []
external_signals: List[ExternalSignal] = []
child_presence: List[ChildPresence] = []
staff_presence: List[StaffPresence] = []
individual_plans = {}

@app.get('/health')
def health():
    return {'status': 'ok', 'version': app.version}

@app.post('/api/v1/observations', status_code=201)
def add_observation(item: Observation):
    observations.append(item)
    return item

@app.post('/api/v1/landscape', status_code=201)
def add_landscape(item: Landscape):
    landscapes.append(item)
    return item

@app.post('/api/v1/safety/signals', status_code=201)
def add_safety_signal(item: SafetySignal):
    safety_signals.append(item)
    return {'accepted': True, 'human_review_required': True, 'signal': item}

@app.post('/api/v1/external/signals', status_code=201)
def add_external_signal(item: ExternalSignal):
    external_signals.append(item)
    return {'accepted': True, 'human_review_required': True, 'signal': item}

@app.get('/api/v1/external/landscape')
def external_landscape():
    return build_external_landscape([x.model_dump() for x in external_signals])

@app.post('/api/v1/presence/children', status_code=201)
def add_child_presence(item: ChildPresence):
    child_presence.append(item)
    return item

@app.post('/api/v1/presence/staff', status_code=201)
def add_staff_presence(item: StaffPresence):
    staff_presence.append(item)
    return item

@app.get('/api/v1/presence/time-landscape')
def presence_time_landscape():
    return build_presence_time_landscape(
        [x.model_dump() for x in child_presence],
        [x.model_dump() for x in staff_presence],
    )

@app.post('/api/v1/children/{child_id}/support-plan', response_model=IndividualSupportPlan, status_code=201)
def create_support_plan(child_id: str, item: IndividualSupportPlan):
    item.child_id = child_id
    individual_plans[child_id] = item
    return item

@app.get('/api/v1/children/{child_id}/support-plan', response_model=IndividualSupportPlan)
def get_support_plan(child_id: str):
    if child_id not in individual_plans:
        raise HTTPException(status_code=404, detail='Individual support plan not found')
    return individual_plans[child_id]

@app.patch('/api/v1/children/{child_id}/support-plan', response_model=IndividualSupportPlan)
def update_support_plan(child_id: str, update: IndividualPlanUpdate):
    if child_id not in individual_plans:
        raise HTTPException(status_code=404, detail='Individual support plan not found')
    current = individual_plans[child_id]
    changes = update.model_dump(exclude_none=True)
    note = changes.pop('revision_note', '')
    for key, value in changes.items():
        setattr(current, key, value)
    if note:
        current.revision_history.append(note)
    current.updated_at = datetime.utcnow()
    return current

@app.get('/api/v1/landscape/daily')
def daily_landscape():
    return {
        'observations': observations[-20:],
        'individual_support_plans': list(individual_plans.values()),
        'landscapes': landscapes[-6:],
        'safety_signals': safety_signals[-20:],
        'facility_landscape': build_facility_landscape(observations, landscapes, safety_signals, individual_plans),
        'presence_time_landscape': build_presence_time_landscape([x.model_dump() for x in child_presence], [x.model_dump() for x in staff_presence]),
        'external_landscape': build_external_landscape([x.model_dump() for x in external_signals]),
        'note': 'AI output is advisory; human review and facility policy remain authoritative.'
    }

@app.get('/api/v1/landscape/facility')
def facility_landscape():
    return build_facility_landscape(observations, landscapes, safety_signals, individual_plans)

@app.post('/api/v1/plans/tomorrow')
def tomorrow_plan():
    facts = [f for o in observations[-10:] for f in o.facts]
    individual_considerations = []
    for plan in individual_plans.values():
        individual_considerations.append({
            'child_id': plan.child_id,
            'goals': plan.goals,
            'support_policy': plan.support_policy,
            'environmental_adjustments': plan.environmental_adjustments,
            'participation_and_choice': plan.participation_and_choice,
            'class_integration_notes': plan.class_integration_notes,
        })
    return {
        'status': 'draft',
        'goals': ['子どもの選択と主体性を確保する', '一斉指示を必要最小限にする'],
        'observed_facts': facts,
        'individual_support_considerations': individual_considerations,
        'facility_landscape': build_facility_landscape(observations, landscapes, safety_signals, individual_plans),
        'presence_time_landscape': build_presence_time_landscape([x.model_dump() for x in child_presence], [x.model_dump() for x in staff_presence]),
        'external_landscape': build_external_landscape([x.model_dump() for x in external_signals]),
        'checkpoints': ['子どもの選択が増えたか', '保育者の一斉指示が減ったか', '安全上の変化はないか'],
        'staffing_considerations': [f'{x.class_id}: 出席{x.attendance}人／配置{x.assigned_staff}人' for x in landscapes[-6:]],
        'safety_considerations': [s.facts for s in safety_signals[-10:]],
        'external_considerations': [s.summary for s in external_signals[-20:]],
        'human_review_required': True
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
