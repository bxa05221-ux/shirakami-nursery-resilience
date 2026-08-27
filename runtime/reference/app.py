from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title='Shirakami Nursery Resilience API', version='0.1.0-alpha1')

class Observation(BaseModel):
    class_id: str
    facts: List[str] = Field(min_length=1)
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

observations: List[Observation] = []
landscapes: List[Landscape] = []
safety_signals: List[SafetySignal] = []

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

@app.get('/api/v1/landscape/daily')
def daily_landscape():
    return {
        'observations': observations[-20:],
        'landscapes': landscapes[-6:],
        'safety_signals': safety_signals[-20:],
        'note': 'AI output is advisory; human review and facility policy remain authoritative.'
    }

@app.post('/api/v1/plans/tomorrow')
def tomorrow_plan():
    facts = [f for o in observations[-10:] for f in o.facts]
    return {
        'status': 'draft',
        'goals': ['子どもの選択と主体性を確保する', '一斉指示を必要最小限にする'],
        'observed_facts': facts,
        'checkpoints': ['子どもの選択が増えたか', '保育者の一斉指示が減ったか', '安全上の変化はないか'],
        'staffing_considerations': [f'{x.class_id}: 出席{x.attendance}人／配置{x.assigned_staff}人' for x in landscapes[-6:]],
        'safety_considerations': [s.facts for s in safety_signals[-10:]],
        'human_review_required': True
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
