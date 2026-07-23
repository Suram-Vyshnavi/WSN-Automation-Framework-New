<#
.SYNOPSIS
    Runs every persona against BOTH dev and prod in one go and produces a single
    combined executive dashboard (the NEN-style stakeholder report).

    Pairs without configured credentials (e.g. a Career Buddy prod account) are
    skipped automatically rather than failed.

.EXAMPLE
    .\run-combined-report.ps1
    .\run-combined-report.ps1 -Personas student,faculty,rm
    .\run-combined-report.ps1 -Envs dev,prod -Headless
#>
param(
    [string[]]$Personas,
    [string[]]$Envs = @("dev", "prod"),
    [switch]$Headless
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) { $python = "python" }

# Force UTF-8 so the status glyphs (▶ ✅ ⏭) don't crash on a cp1252 console.
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$env:RUN_MODE = "matrix"
$env:ENVS = ($Envs -join ",")
if ($Envs.Count -eq 1) { $env:ENV = $Envs[0] }
if ($Personas) { $env:PERSONAS = ($Personas -join ",") } else { Remove-Item Env:\PERSONAS -ErrorAction SilentlyContinue }
if ($Headless) { $env:HEADLESS = "true" } else { $env:HEADLESS = "false" }

Write-Host "Running combined matrix | envs='$($env:ENVS)' | personas='$($env:PERSONAS)'" -ForegroundColor Cyan

& $python "$root\run_tests.py"
$code = $LASTEXITCODE

$dashboard = Join-Path $root "reports\allure-report-combined\executive-dashboard-combined.html"
Write-Host "Done (exit=$code)." -ForegroundColor Green
Write-Host "  combined dashboard -> $dashboard" -ForegroundColor DarkCyan
exit $code
