<#
Register a Windows Task Scheduler job that runs `polymarket snapshot` every 15 minutes.

Run this script ONCE in PowerShell to register the task. Re-run with -Unregister to remove.
The task runs in the current user's context (no elevation required) and writes a rotating
log to data/logs/snapshot.log under the project root.

Usage:
  .\scripts\windows_task.ps1                # register the 15-min recurrence
  .\scripts\windows_task.ps1 -Unregister    # remove the scheduled task
  .\scripts\windows_task.ps1 -RunNow        # register and trigger one immediate run
#>

param(
    [switch]$Unregister,
    [switch]$RunNow
)

$ErrorActionPreference = 'Stop'

$TaskName = 'PolymarketModelSnapshot'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$LogDir = Join-Path $ProjectRoot 'data\logs'
$LogPath = Join-Path $LogDir 'snapshot.log'
$UvCmd = (Get-Command uv -ErrorAction SilentlyContinue).Source
if (-not $UvCmd) {
    $UserPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')
    $MachinePath = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
    $env:Path = "$UserPath;$MachinePath"
    $UvCmd = (Get-Command uv -ErrorAction SilentlyContinue).Source
}
if (-not $UvCmd) {
    throw "uv was not found on PATH. Install via 'winget install astral-sh.uv' first."
}

if ($Unregister) {
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "Unregistered scheduled task: $TaskName"
    } else {
        Write-Host "No task named $TaskName was registered."
    }
    return
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

$Cmd = "Set-Location -LiteralPath '$ProjectRoot'; & '$UvCmd' run polymarket snapshot --quiet *>> '$LogPath'"
$Action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -Command `"$Cmd`""
$Trigger = New-ScheduledTaskTrigger -Once -At ((Get-Date).AddMinutes(1)) `
    -RepetitionInterval (New-TimeSpan -Minutes 15)
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Set-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings | Out-Null
    Write-Host "Updated scheduled task: $TaskName"
} else {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal `
        -Description 'Polymarket weather model: 15-min midpoint+book snapshot recorder.' | Out-Null
    Write-Host "Registered scheduled task: $TaskName (every 15 minutes, current user, no admin)"
}

Write-Host "Logs: $LogPath"
Write-Host "Note: snapshots will pause when this machine is asleep."

if ($RunNow) {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "Triggered an immediate run."
}
