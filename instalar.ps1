# Instalador de las Publiqo Edición para Windows: todas las skills y todo lo necesario para editar y renderizar.
# Desde PowerShell (no hace falta ser administrador):
#   irm https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar.ps1 | iex
# o, con opciones (carpeta de edición y creador que viene incluido):
#   & ([scriptblock]::Create((irm https://raw.githubusercontent.com/lucasalvarezblancob-ux/publiqo-edicion/main/instalar.ps1))) -Carpeta "$HOME\Desktop\Horizontal" -Creador reinoselva
#
# Hace: instala con winget lo que falte (Git, ffmpeg completo, Node LTS, Python 3.12, yt-dlp, GitHub CLI, mpv y
# Claude Code); descarga el repo en ~\Projects\publiqo-edicion (o lo actualiza); enlaza todas sus skills en
# ~\.claude\skills y deja el hook que las actualiza solas (y añade las nuevas); y lanza edicion-horizontal/instalar.sh:
# la carpeta de edición, las skills de apoyo (Remotion, HyperFrames), la .venv de Python (con CUDA si hay NVIDIA),
# node_modules y el navegador de render. Con -Creador, además deja su personalización y enlaza sus recursos al disco.
param(
  [string]$Carpeta = "$HOME\Desktop\Horizontal",
  [string]$Creador = "",
  [string]$Skill = "$HOME\Projects\publiqo-edicion"
)
$ErrorActionPreference = "Stop"
$Repo = "https://github.com/lucasalvarezblancob-ux/publiqo-edicion.git"

function Refrescar-Path {
  $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:LOCALAPPDATA\Microsoft\WinGet\Links;$HOME\.local\bin"
}
function Hay($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Python-Ok {
  foreach ($c in "python", "py") {
    if (Hay $c) { & $c -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>$null; if ($LASTEXITCODE -eq 0) { return $true } }
  }
  return $false
}

if (-not (Hay "winget")) { throw "Falta winget (Instalador de aplicaciones). Instálalo desde Microsoft Store y vuelve a lanzar." }

Write-Host "-> Programas (solo los que falten)"
$programas = @(
  @{ Cmd = "git";    Id = "Git.Git" },
  @{ Cmd = "ffmpeg"; Id = "Gyan.FFmpeg" },              # versión completa: trae libplacebo (brutos HDR del iPhone)
  @{ Cmd = "node";   Id = "OpenJS.NodeJS.LTS" },
  @{ Cmd = "python"; Id = "Python.Python.3.12" },
  @{ Cmd = "yt-dlp"; Id = "yt-dlp.yt-dlp" },
  @{ Cmd = "gh";     Id = "GitHub.cli" },
  @{ Cmd = "mpv";    Id = "shinchiro.mpv" }
)
foreach ($p in $programas) {
  $falta = if ($p.Cmd -eq "python") { -not (Python-Ok) } elseif ($p.Cmd -eq "mpv") { -not (Hay "mpv") -and -not (Test-Path "C:\Program Files\MPV Player\mpv.exe") } else { -not (Hay $p.Cmd) }
  if ($falta) {
    Write-Host "   instalando $($p.Id)"
    winget install -e --id $p.Id --silent --accept-package-agreements --accept-source-agreements | Out-Null
    Refrescar-Path
  }
}
Refrescar-Path

if (-not (Hay "claude")) {
  Write-Host "-> Claude Code"
  try { Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression; Refrescar-Path } catch { Write-Warning "No se pudo instalar Claude Code: https://claude.com/claude-code" }
}

foreach ($c in "git", "ffmpeg", "node") { if (-not (Hay $c)) { throw "Falta $c tras instalarlo. Cierra PowerShell, ábrelo de nuevo y vuelve a lanzar." } }
if (-not (Python-Ok)) { throw "Falta Python 3.10+ tras instalarlo. Cierra PowerShell, ábrelo de nuevo y vuelve a lanzar." }

Write-Host "-> Publiqo Edición en $Skill"
if (Test-Path "$Skill\.git") { git -C $Skill pull -q --ff-only origin main }
else { New-Item -ItemType Directory -Force (Split-Path $Skill) | Out-Null; git clone -q $Repo $Skill }

$bash = Join-Path (Split-Path (Split-Path (Get-Command git).Source)) "bin\bash.exe"
if (-not (Test-Path $bash)) { $bash = "C:\Program Files\Git\bin\bash.exe" }
if (-not (Test-Path $bash)) { throw "No encuentro Git Bash (bash.exe)." }

Write-Host "-> Todas las skills (enlazadas en ~\.claude\skills) y actualización automática"
$env:PUBLIQO_ED_SIN_AVISOS = "1"
& $bash ("$Skill/sincronizar.sh".Replace('\', '/')) --ya
Remove-Item Env:PUBLIQO_ED_SIN_AVISOS
$py = if (Hay "python") { "python" } else { "py" }
& $py "$Skill\hook_global.py" $Skill

Write-Host "-> edicion-horizontal: carpeta de edición"
$args_sh = @(("$Skill/edicion-horizontal/instalar.sh").Replace('\', '/'))
if (Test-Path "$Carpeta\personal\LEEME.md") { $args_sh += "--adoptar" }
if ($Creador) { $args_sh += @("--creador", $Creador) }
$args_sh += $Carpeta.Replace('\', '/')
& $bash @args_sh
if ($LASTEXITCODE -ne 0) { throw "instalar.sh terminó con error (mira arriba)." }

Write-Host ""
Write-Host "Listo. Abre la carpeta con Claude Code:  cd `"$Carpeta`"; claude"
