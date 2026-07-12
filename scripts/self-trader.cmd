@echo off
REM Runner for the Windows Scheduled Task "SelfTrader" (hourly, same cadence as the
REM kalshi-live production trader; quiet hours exit fast per the prompt's fast path).
REM Runs the /self-trader agent headless: settles its paper book, grades its own
REM strategy against outcomes, revises data/agent/strategy.md, scans ALL Kalshi
REM markets, opens new paper trades via the guarded agent-trade CLI, journals, and
REM commits ONLY data/agent/ back to main. PAPER ONLY - no order code exists in
REM this repo. Logs to data/agent/self-trader.log (gitignored via *.log).

cd /d "%~dp0.."
set PYTHONIOENCODING=utf-8
echo ==== %DATE% %TIME% SELF-TRADER ======================== >> "data\agent\self-trader.log"
"C:\Users\Sean\.local\bin\claude.exe" -p "/self-trader" --permission-mode acceptEdits >> "data\agent\self-trader.log" 2>&1
echo. >> "data\agent\self-trader.log"
