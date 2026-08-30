$ErrorActionPreference = 'Stop'

if (-not (Test-Path '.venv\Scripts\python.exe')) {
    throw 'Pilot is not installed. Run .\scripts\install-pilot.ps1 first.'
}

Write-Host 'Starting Shirakami Nursery Resilience Alpha 1.0 reference API...'
Write-Host 'Open http://127.0.0.1:8000/api/v1/landscape/daily in your browser.'
Write-Host 'Press Ctrl+C to stop.'
& .\.venv\Scripts\python.exe runtime\reference\server.py
