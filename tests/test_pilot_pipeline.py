import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime' / 'reference'))

from pilot_pipeline import run_pilot


def test_synthetic_pilot_end_to_end():
    path = ROOT / 'examples' / 'pilot' / 'sample-facility.yaml'
    dataset = yaml.safe_load(path.read_text(encoding='utf-8'))
    result = run_pilot(dataset)

    assert result['synthetic'] is True
    assert result['facility_id'] == 'FACILITY-DEMO-001'
    assert result['presence_time_landscape']['time_slots']
    assert result['time_window_forecast']['time_windows']
    assert result['human_review_required'] is True


def test_forecast_retains_source_and_uncertainty():
    path = ROOT / 'examples' / 'pilot' / 'sample-facility.yaml'
    dataset = yaml.safe_load(path.read_text(encoding='utf-8'))
    result = run_pilot(dataset)
    window = result['time_window_forecast']['time_windows'][0]

    assert window['source'] == 'synthetic-demo'
    assert window['probability_or_confidence'] == 0.7
