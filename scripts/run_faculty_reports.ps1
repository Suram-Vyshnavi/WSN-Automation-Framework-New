param(
    [switch]$DryRun,
    [string]$Env = "qa",
    [switch]$SkipBatchCreation
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$RunnerScript = Join-Path $ProjectRoot "scripts\run_persona_reports.py"

if (!(Test-Path $PythonExe)) {
    Write-Error "Python executable not found at: $PythonExe"
}

if (!(Test-Path $RunnerScript)) {
    Write-Error "Runner script not found at: $RunnerScript"
}

$runArgs = @("--persona", "faculty")
if ($SkipBatchCreation) {
    $runArgs += @("--exclude-tags", "faculty_only")
}

$cmd = "`"$PythonExe`" `"$RunnerScript`" $($runArgs -join ' ')"

Write-Host "Project Root: $ProjectRoot"
Write-Host "Env:          $Env"
Write-Host "Command:      $cmd"

if ($DryRun) {
    Write-Host "Dry run enabled. No test execution performed."
    exit 0
}

$env:ENV = $Env
& $PythonExe $RunnerScript @runArgs
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Host "Faculty run completed with failures (exit code: $exitCode). Reports are still generated from available results."
} else {
    Write-Host "Faculty run completed successfully."
}

Write-Host "HTML: reports/allure-report-faculty/index.html"
Write-Host "PDF:  reports/allure-report-faculty/allure-report-faculty-full.pdf"

exit $exitCode
