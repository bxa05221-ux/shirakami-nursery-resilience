from pathlib import Path
from typing import Any, Dict
import yaml

from presence_time import build_presence_time_landscape
from time_window_forecast import build_time_window_forecast


def load_sample_dataset(path: str) -> Dict[str, Any]:
    with Path(path).open(encoding='utf-8') as f:
        return yaml.safe_load(f)


def run_pilot(dataset: Dict[str, Any]) -> Dict[str, Any]:
    facility = dataset['facility']
    children = facility.get('children', [])
    staff = facility.get('staff', [])
    external_events = facility.get('external_events', [])
    activities = facility.get('planned_activities', [])

    presence = build_presence_time_landscape(children, staff)
    forecast = build_time_window_forecast(external_events, presence, activities)

    return {
        'facility_id': facility['facility_id'],
        'synthetic': True,
        'presence_time_landscape': presence,
        'time_window_forecast': forecast,
        'planned_activities': activities,
        'human_review_required': True,
    }
