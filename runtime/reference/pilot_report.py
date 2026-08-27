from typing import Any, Dict


def render_pilot_report(result: Dict[str, Any]) -> Dict[str, Any]:
    """Render a concise, human-reviewable daily landscape report."""
    presence = result.get('presence_time_landscape', {})
    forecast = result.get('time_window_forecast', {})

    class_totals = {}
    for slot in presence.get('time_slots', []):
        for class_id, count in slot.get('children_present_by_class', {}).items():
            class_totals[class_id] = max(class_totals.get(class_id, 0), count)

    return {
        'report_title': '明日の保育Landscape — パイロット表示',
        'facility_id': result.get('facility_id'),
        'synthetic_data': result.get('synthetic', False),
        'class_peak_children': class_totals,
        'time_windows': [
            {
                'time': w.get('start') + ' - ' + w.get('end') if w.get('start') and w.get('end') else None,
                'condition': w.get('phenomenon'),
                'confidence': w.get('probability_or_confidence'),
                'source': w.get('source'),
                'review': w.get('recommended_review'),
            }
            for w in forecast.get('time_windows', [])
        ],
        'planned_activities': result.get('planned_activities', []),
        'decision_status': 'human_review_required',
        'disclaimer': '予測は判断材料です。現況、安全情報、園の規程・配置基準を確認して保育者が判断します。',
    }
