# Capture a real console screenshot of a command run from the repository root.
# Opens a new console window, runs the command in it, then grabs the window's
# own bitmap with PrintWindow so overlapping windows cannot bleed in.
param(
    [Parameter(Mandatory = $true)][string]$Command,
    [Parameter(Mandatory = $true)][string]$OutFile,
    [int]$Width = 118,
    [int]$Height = 40,
    [int]$WaitSeconds = 7
)

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win {
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left, Top, Right, Bottom; }
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT r);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int n);
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hWnd, IntPtr hdc, uint flags);
}
"@ -ErrorAction SilentlyContinue
[Win]::SetProcessDPIAware() | Out-Null   # measure in real pixels on a scaled display

$repo = Split-Path -Parent $PSScriptRoot
$title = "RIDE-CAPTURE-" + [Guid]::NewGuid().ToString("N").Substring(0, 8)
# The buffer is made exactly the window size so no scrollbar covers the last
# columns (shrink the window first; a buffer cannot be smaller than it).
$ps = @"
`$Host.UI.RawUI.WindowTitle = '$title'
`$Host.UI.RawUI.WindowSize  = New-Object Management.Automation.Host.Size(40, 10)
`$Host.UI.RawUI.BufferSize = New-Object Management.Automation.Host.Size($Width, $Height)
`$Host.UI.RawUI.WindowSize  = New-Object Management.Automation.Host.Size($Width, $Height)

Set-Location '$repo'
Clear-Host
$Command
"@

$enc = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($ps))
$p = Start-Process conhost.exe -ArgumentList 'powershell.exe', '-NoLogo', '-NoProfile', '-NoExit', '-EncodedCommand', $enc -PassThru
Start-Sleep -Seconds $WaitSeconds

# The console window belongs to the hosted powershell child, not to conhost.
$h = [IntPtr]::Zero
$owner = $null
for ($i = 0; $i -lt 25; $i++) {
    $owner = Get-Process | Where-Object { $_.MainWindowTitle -eq $title } | Select-Object -First 1
    if ($owner -and $owner.MainWindowHandle -ne [IntPtr]::Zero) { $h = $owner.MainWindowHandle; break }
    Start-Sleep -Milliseconds 400
}
if ($h -eq [IntPtr]::Zero) {
    $p | Stop-Process -Force -ErrorAction SilentlyContinue
    throw "no window handle for $OutFile"
}

[Win]::ShowWindow($h, 9) | Out-Null      # SW_RESTORE
[Win]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 1200

$r = New-Object Win+RECT
[Win]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.Right - $r.Left
$hh = $r.Bottom - $r.Top
$bmp = New-Object System.Drawing.Bitmap($w, $hh)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$hdc = $g.GetHdc()
$ok = [Win]::PrintWindow($h, $hdc, 2)   # 2 = PW_RENDERFULLCONTENT, needed for consoles
$g.ReleaseHdc($hdc)

$dir = Split-Path -Parent $OutFile
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$bmp.Save($OutFile, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()

$p | Stop-Process -Force -ErrorAction SilentlyContinue
if ($owner) { $owner | Stop-Process -Force -ErrorAction SilentlyContinue }
Write-Output ("saved {0}  ({1}x{2})  printwindow={3}" -f $OutFile, $w, $hh, $ok)
