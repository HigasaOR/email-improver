# Email & Text Improver - Windows launch script
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# Add common uv install locations to PATH
$env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"

# Install uv if missing
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv..."
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    # Pick up the newly added PATH entry
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + $env:PATH
}

# First-run setup
if (-not (Test-Path ".venv")) {
    Write-Host "Setting up environment (first run)..."
    uv python install 3.13
    uv venv --python 3.13
    uv pip install -r requirements.txt
}

# Launch
& ".venv\Scripts\python.exe" main.py
