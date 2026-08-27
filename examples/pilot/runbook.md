# Synthetic Pilot Runbook

## Purpose
Validate the Alpha 1.0 loop before any real nursery data is introduced.

## Sequence
1. Load `examples/pilot/sample-facility.yaml`.
2. Run the reference pilot pipeline.
3. Generate the human-readable pilot report.
4. Verify presence/time landscape, external time windows, and planned activities.
5. Confirm `human_review_required` remains true.
6. Confirm synthetic data is the only data used.
7. Review access, anonymization, and evidence boundaries.
8. Record findings as pilot observations; do not treat them as production validation.

## Stop conditions
- Any real personal data appears in the dataset.
- Identity mapping appears outside the protected identity boundary.
- AI output is represented as a human decision.
- Forecast source or uncertainty is lost.
- Staffing or safety decisions are made automatically.
- A required facility rule or statutory requirement is unknown.

## Exit criteria
- Pipeline completes without error.
- Report is understandable to a human reviewer.
- Privacy boundaries are preserved.
- Evidence provenance is retained.
- Known gaps are recorded for the next iteration.
