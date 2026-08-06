@echo off
rem ────────────────────────────────────────────────────────────
rem  Preview the site on your own machine.
rem  Double-click this file, then open  http://localhost:1313
rem  in your browser. Press Ctrl+C in this window to stop.
rem
rem  First time only: put hugo.exe next to this file.
rem  Download "hugo_extended_0.164.0_windows-amd64.zip" from
rem  https://github.com/gohugoio/hugo/releases/tag/v0.164.0
rem  and copy the hugo.exe from inside it into this folder.
rem ────────────────────────────────────────────────────────────
rem The pinned copy beside this file wins over any hugo on PATH,
rem so the preview always matches the version the site was built for.
if exist "%~dp0hugo.exe" (
  "%~dp0hugo.exe" server --navigateToChanged
  goto :eof
)
where hugo >nul 2>nul
if %errorlevel%==0 (
  echo.
  echo   NOTE: no hugo.exe found beside this script; using the hugo on
  echo   your PATH instead, which may not be the pinned 0.164.0 the site
  echo   was built for. If the preview misbehaves, download the pinned
  echo   version ^(see the note at the top of this file^).
  echo.
  hugo server --navigateToChanged
) else (
  echo.
  echo   hugo.exe was not found.
  echo   Download it once from:
  echo   https://github.com/gohugoio/hugo/releases/tag/v0.164.0
  echo   ^(file: hugo_extended_0.164.0_windows-amd64.zip^)
  echo   Unzip it and place hugo.exe in this folder, then run me again.
  echo.
  pause
)
