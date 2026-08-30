$ErrorActionPreference = 'Stop'

Write-Host 'Shirakami Nursery Resilience - Alpha 1.0 Pilot installer'

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw 'Python launcher (py) was not found. Install Python 3.11 and try again.'
}

$python = & py -3.11 -c "import sys; print(sys.executable)"
if ($LASTEXITCODE -ne 0) {
    throw 'Python 3.11 was not found. Install Python 3.11 and try again.'
}

if (-not (Test-Path '.venv')) {
    & py -3.11 -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m pip install pytest

& .\.venv\Scripts\python.exe -m compileall runtime/reference
& .\.venv\Scripts\python.exe -m pytest -q tests/test_pilot_pipeline.py

Write-Host ''
Write-Host 'Pilot installation and Synthetic Pilot check completed.'
Write-Host 'Start the local reference API with:'
Write-Host '  .\.venv\Scripts\python.exe runtime\reference\server.py'
Write-Host 'Then open: http://127.0.0.1:8000/api/v1/landscape/daily'
Write-Host ''
Write-Host 'WARNING: The reference runtime is not production-ready and must not receive real child/staff personal data.'
