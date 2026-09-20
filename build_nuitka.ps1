[CmdletBinding()]
param(
    [string]$OutputDir = 'dist',
    [switch]$SkipUvSync
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$helpDir = Join-Path $root 'help'
$pluginsDir = Join-Path $root 'plugins'

Push-Location $root
try {
    if (-not $SkipUvSync) {
        & uv sync --group build --no-dev
        if ($LASTEXITCODE -ne 0) { throw 'uv sync failed' }
    }

    $options = @(
        '--enable-plugin=tk-inter',
        '--include-package=sltgui',
        '--include-package-data=sltgui',
        '--include-package=lupa',
        "--include-data-dir=$helpDir=help",
        "--include-data-dir=$pluginsDir=plugins",
        '--assume-yes-for-downloads',
        "--output-dir=$OutputDir",
        '--output-filename=StructLayoutToolkit',
        '--standalone'
    )
    if ($IsWindows) {
        $options += '--windows-console-mode=disable'
    }

    & uv run python -m nuitka @options launcher.py
    if ($LASTEXITCODE -ne 0) { throw 'Nuitka build failed' }
}
finally {
    Pop-Location
}