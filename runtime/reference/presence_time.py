from collections import defaultdict
from datetime import datetime


def _hour_slots(start_hour=7, end_hour=19):
    return [f'{h:02d}:00-{h+1:02d}:00' for h in range(start_hour, end_hour)]


def _parse_datetime(value):
    if isinstance(value, datetime):
        return value
    if not value:
        return None
    return datetime.fromisoformat(value)


def _infer_target_date(child_presence, staff_presence):
    for record in [*child_presence, *staff_presence]:
        for key in ('actual_arrival', 'scheduled_arrival', 'actual_start', 'scheduled_start'):
            parsed = _parse_datetime(record.get(key))
            if parsed:
                return parsed.date()
    return None


def build_presence_time_landscape(child_presence, staff_presence, class_ids=None, start_hour=7, end_hour=19):
    """Build an observational time landscape from child/staff presence records."""
    class_ids = class_ids or sorted({x.get('class_id') for x in child_presence if x.get('class_id')})
    slots = _hour_slots(start_hour, end_hour)
    target_date = _infer_target_date(child_presence, staff_presence)
    hourly = []

    for slot in slots:
        hour = int(slot[:2])
        point = datetime.combine(target_date, datetime.min.time()).replace(hour=hour) if target_date else None
        children_by_class = defaultdict(int)
        staff_by_class = defaultdict(int)

        for child in child_presence:
            arrival = _parse_datetime(child.get('actual_arrival') or child.get('scheduled_arrival'))
            departure = _parse_datetime(child.get('actual_departure') or child.get('scheduled_departure'))
            if not arrival or not departure or not point:
                continue
            if arrival.date() == target_date and departure.date() == target_date and arrival <= point < departure and child.get('status') not in ('absent',):
                children_by_class[child.get('class_id', 'unassigned')] += 1

        for staff in staff_presence:
            start = _parse_datetime(staff.get('actual_start') or staff.get('scheduled_start'))
            end = _parse_datetime(staff.get('actual_end') or staff.get('scheduled_end'))
            if not start or not end or not point:
                continue
            if start.date() == target_date and end.date() == target_date and start <= point < end:
                for class_id in staff.get('assigned_class_ids', []):
                    staff_by_class[class_id] += 1

        hourly.append({'time_slot': slot, 'children_present_by_class': dict(children_by_class), 'staff_present_by_class': dict(staff_by_class)})

    return {
        'scope': 'facility',
        'time_slots': hourly,
        'class_ids': class_ids,
        'generated_at': datetime.utcnow().isoformat(),
        'human_review_required': True,
        'note': 'Observed presence is a landscape signal; statutory staffing rules and facility policy remain authoritative.'
    }
