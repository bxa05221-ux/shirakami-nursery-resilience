from collections import defaultdict
from datetime import datetime, timedelta


def _hour_slots(start_hour=7, end_hour=19):
    return [f'{h:02d}:00-{h+1:02d}:00' for h in range(start_hour, end_hour)]


def build_presence_time_landscape(child_presence, staff_presence, class_ids=None, start_hour=7, end_hour=19):
    """Build an observational time landscape from child/staff presence records.

    This function reports observed/scheduled presence. It does not determine
    statutory staffing compliance or make autonomous staffing decisions.
    """
    class_ids = class_ids or sorted({x.get('class_id') for x in child_presence if x.get('class_id')})
    slots = _hour_slots(start_hour, end_hour)
    hourly = []

    for slot in slots:
        hour = int(slot[:2])
        point = datetime(2000, 1, 1, hour)
        children_by_class = defaultdict(int)
        staff_by_class = defaultdict(int)

        for child in child_presence:
            arrival = child.get('actual_arrival') or child.get('scheduled_arrival')
            departure = child.get('actual_departure') or child.get('scheduled_departure')
            if not arrival or not departure:
                continue
            if arrival <= point < departure and child.get('status') not in ('absent',):
                class_id = child.get('class_id', 'unassigned')
                children_by_class[class_id] += 1

        for staff in staff_presence:
            start = staff.get('actual_start') or staff.get('scheduled_start')
            end = staff.get('actual_end') or staff.get('scheduled_end')
            if not start or not end:
                continue
            if start <= point < end:
                for class_id in staff.get('assigned_class_ids', []):
                    staff_by_class[class_id] += 1

        hourly.append({
            'time_slot': slot,
            'children_present_by_class': dict(children_by_class),
            'staff_present_by_class': dict(staff_by_class),
        })

    return {
        'scope': 'facility',
        'time_slots': hourly,
        'class_ids': class_ids,
        'generated_at': datetime.utcnow().isoformat(),
        'human_review_required': True,
        'note': 'Observed presence is a landscape signal; statutory staffing rules and facility policy remain authoritative.'
    }
