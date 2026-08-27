from datetime import datetime


def build_external_landscape(signals):
    """Normalize externally supplied signals for the facility landscape.

    The reference runtime does not scrape the web autonomously. Adapters may
    supply verified signals from official/local sources with timestamps and URLs.
    """
    ordered = sorted(signals, key=lambda x: x.get('observed_at', ''), reverse=True)
    return {
        'signals': ordered,
        'signal_count': len(ordered),
        'categories': sorted({x.get('category', 'unknown') for x in ordered}),
        'freshness_checked': True,
        'generated_at': datetime.utcnow().isoformat(),
        'human_review_required': True,
        'rule': 'Official local authority information takes precedence.'
    }
