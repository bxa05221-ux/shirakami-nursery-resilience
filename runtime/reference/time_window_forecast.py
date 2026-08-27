from collections import defaultdict
from datetime import datetime


def build_time_window_forecast(external_events, presence_landscape=None, planned_activities=None):
    """Normalize external events into planning time windows.

    Events are contextual evidence only. This function does not decide whether
    an activity should occur.
    """
    windows = []
    for event in external_events:
        windows.append({
            'start': event.get('start'),
            'end': event.get('end'),
            'phenomenon': event.get('phenomenon'),
            'probability_or_confidence': event.get('probability_or_confidence'),
            'source': event.get('source'),
            'impact_candidates': event.get('impact_candidates', []),
            'recommended_review': event.get('recommended_review'),
        })

    return {
        'scope': 'facility',
        'generated_at': datetime.utcnow().isoformat(),
        'time_windows': windows,
        'context': {
            'presence_landscape_available': presence_landscape is not None,
            'planned_activities_available': planned_activities is not None,
        },
        'human_review_required': True,
        'note': 'Forecasts are planning aids. Recheck current conditions; facility policy and safety rules remain authoritative.'
    }
