# Regenerate the console screenshots used in the report (Windows + WSL).
# Each program prints 57 lines, more than a console window shows on this
# display, so each run is captured in two parts with Select-Object. The
# programs have no randomness, so both parts come from identical output.
# Code screenshots come from tools/code_shots.py.
$tools = $PSScriptRoot
$out = Join-Path (Split-Path -Parent $tools) "report\screenshots"
New-Item -ItemType Directory -Force -Path $out | Out-Null

function Console($name, $cmd, $height = 37, $wait = 8) {
    & "$tools\capture_console.ps1" -Command $cmd -OutFile (Join-Path $out $name) -Width 104 -Height $height -WaitSeconds $wait
}

Console "10_cpp_run_part1.png" @'
Write-Host "PS $PWD> wsl make -s -C cpp clean ride_sharing"
wsl -d Ubuntu make -s -C cpp clean ride_sharing
Write-Host "PS $PWD> wsl ./cpp/ride_sharing | Select-Object -First 31"
wsl -d Ubuntu ./cpp/ride_sharing | Select-Object -First 31
'@ 37 12

Console "11_cpp_run_part2.png" @'
Write-Host "PS $PWD> wsl ./cpp/ride_sharing | Select-Object -Skip 31"
wsl -d Ubuntu ./cpp/ride_sharing | Select-Object -Skip 31
'@ 30

Console "12_st_run_part1.png" @'
Write-Host "PS $PWD> wsl bash smalltalk/run.sh | Select-Object -First 31"
wsl -d Ubuntu bash smalltalk/run.sh | Select-Object -First 31
'@ 35

Console "13_st_run_part2.png" @'
Write-Host "PS $PWD> wsl bash smalltalk/run.sh | Select-Object -Skip 31"
wsl -d Ubuntu bash smalltalk/run.sh | Select-Object -Skip 31
'@ 30

Console "14_compare.png" @'
Write-Host "PS $PWD> wsl bash tools/make_outputs.sh"
wsl -d Ubuntu bash tools/make_outputs.sh
'@ 10 12   # 10 rows at least: capture_console shrinks the window to 10 rows first
