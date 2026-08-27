# Synthetic Pilot Run

This directory contains a fictional pilot dataset for validating the Alpha 1.0 reference runtime before any real childcare data is introduced.

## Safety boundary

- The dataset contains no real child, guardian, staff, or facility identity.
- Do not replace the synthetic identifiers with real names in this repository.
- Real deployment requires facility-specific privacy, security, staffing, and statutory validation.

## Pilot flow

1. Load `sample-facility.yaml`.
2. Run the reference pipeline in `runtime/reference/pilot_pipeline.py`.
3. Render the result with `runtime/reference/pilot_report.py`.
4. Verify presence/time landscape, time-window forecast, planned activities, source traceability, and human-review status.
5. Record defects and missing workflows as pilot findings rather than silently changing the source data.

## Expected behavior

The runtime should organize information into a human-reviewable landscape. It must not autonomously approve activities, alter staffing, identify a pseudonymized person, or close a safety/whistleblower case.
