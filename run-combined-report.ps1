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
    .\run-combined-report.ps1 -Envs prod -Headless -SendEmail
    .\run-combined-report.ps1 -Envs prod -SendEmail -DryRunEmail   # preview only
#>
param(
    [string[]]$Personas,
    [string[]]$Envs = @("dev", "prod"),
    [switch]$Headless,
    # Mail the execution summary (with the generated dashboard attached) through
    # Microsoft Graph once the run finishes - regardless of the test exit code.
    [switch]$SendEmail,
    # Compose the mail and write it to reports\email-preview.html without sending.
    [switch]$DryRunEmail
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

# Report sharing runs even when $code is non-zero: a run with failures is the
# one stakeholders most need to see.
if ($SendEmail -or $DryRunEmail) {
    Write-Host "Composing execution summary email..." -ForegroundColor Cyan
    $mailArgs = @(
        "$root\scripts\send_report_email.py",
        "--results-dir", "$root\reports\allure-results-combined",
        "--report", $dashboard,
        "--env", $Envs[0],
        "--persona", "combined"
    )
    if ($DryRunEmail) { $mailArgs += "--dry-run" }
    & $python @mailArgs
    if ($LASTEXITCODE -ne 0) { Write-Host "Email step reported exit=$LASTEXITCODE" -ForegroundColor Yellow }
}

exit $code
