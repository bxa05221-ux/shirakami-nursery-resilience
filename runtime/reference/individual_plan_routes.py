from fastapi import APIRouter, HTTPException
from .models.individual_support_plan import IndividualSupportPlan, IndividualPlanUpdate

router = APIRouter(prefix='/api/v1/children', tags=['Individual Support Plans'])
plans = {}

@router.post('/{child_id}/support-plan', response_model=IndividualSupportPlan, status_code=201)
def create_plan(child_id: str, plan: IndividualSupportPlan):
    plan.child_id = child_id
    plans[child_id] = plan
    return plan

@router.get('/{child_id}/support-plan', response_model=IndividualSupportPlan)
def get_plan(child_id: str):
    if child_id not in plans:
        raise HTTPException(status_code=404, detail='Individual support plan not found')
    return plans[child_id]

@router.patch('/{child_id}/support-plan', response_model=IndividualSupportPlan)
def update_plan(child_id: str, update: IndividualPlanUpdate):
    if child_id not in plans:
        raise HTTPException(status_code=404, detail='Individual support plan not found')
    current = plans[child_id]
    changes = update.model_dump(exclude_none=True)
    note = changes.pop('revision_note', '')
    for key, value in changes.items():
        setattr(current, key, value)
    if note:
        current.revision_history.append(note)
    return current
