from collections import Counter


def build_facility_landscape(observations, landscapes, safety_signals, individual_plans):
    """Aggregate class-level observations into a facility-level landscape.

    This is an observation/aggregation layer, not an autonomous childcare decision-maker.
    """
    class_counts = Counter(x.class_id for x in observations)
    safety_counts = Counter(x.signal_type for x in safety_signals)
    staffing = [
        {
            'class_id': x.class_id,
            'attendance': x.attendance,
            'assigned_staff': x.assigned_staff,
            'staffing_note': x.note,
        }
        for x in landscapes[-6:]
    ]

    return {
        'scope': 'facility',
        'class_count_observed': len(set(x.class_id for x in landscapes + observations)),
        'observation_count_by_class': dict(class_counts),
        'active_individual_support_plans': sum(1 for x in individual_plans.values() if x.status == 'active'),
        'safety_signal_counts': dict(safety_counts),
        'staffing': staffing,
        'phase_rotation': {
            'space': ['individual', 'class', 'facility', 'external'],
            'time': ['past', 'present', 'tomorrow'],
        },
        'review_prompts': [
            '複数クラスに共通する変化はあるか',
            '特定クラスだけに現れている変化はあるか',
            '個別支援がクラス環境にどのような影響を与えているか',
            '配置と活動内容の組み合わせに注意すべき変化はあるか',
            'まだ観測できていない関係は何か',
        ],
        'human_review_required': True,
    }
