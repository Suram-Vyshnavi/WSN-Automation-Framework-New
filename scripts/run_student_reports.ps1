param(
    [switch]$DryRun,
    [string]$Env = "qa",
    [string]$ProductVersion = ""
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

$runArgs = @("--persona", "student")
if ($ProductVersion) {
    $runArgs += @("--product-version", $ProductVersion)
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
    Write-Host "Student run completed with failures (exit code: $exitCode). Reports are still generated from available results."
} else {
    Write-Host "Student run completed successfully."
}

Write-Host "HTML: reports/allure-report-student/index.html"
Write-Host "PDF:  reports/allure-report-student/allure-report-student-full.pdf"

exit $exitCode
