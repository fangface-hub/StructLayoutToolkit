[CmdletBinding()]
param(
    [string]$InputDistPath = 'dist/launcher.dist',
    [string]$ManifestPath = 'AppxManifest.xml',
    [string]$OutputMsixPath = 'dist/StructLayoutToolkit.msix',
    [string]$StageDir = 'dist/msix',
    [string]$Publisher = 'CN=PLACEHOLDER_PUBLISHER',
    [string]$IdentityName = 'PLACEHOLDER_IDENTITY_NAME',
    [string]$PublisherDisplayName = 'Publisher',
    [string]$MakeAppxPath
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

function Find-MakeAppx {
    $command = Get-Command makeappx.exe -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }
    $kits = 'C:\Program Files (x86)\Windows Kits\10\bin'
    if (-not (Test-Path -LiteralPath $kits)) { return $null }
    Get-ChildItem $kits -Directory |
        Sort-Object Name -Descending |
        ForEach-Object {
            $candidate = Join-Path $_.FullName 'x64\makeappx.exe'
            if (Test-Path -LiteralPath $candidate) { return $candidate }
        }
}

Push-Location $root
try {
    if (-not (Test-Path -LiteralPath $InputDistPath)) {
        throw "Nuitka output not found: $InputDistPath"
    }
    if (-not $MakeAppxPath) { $MakeAppxPath = Find-MakeAppx }
    if (-not $MakeAppxPath) { throw 'makeappx.exe was not found' }

    $project = Get-Content pyproject.toml -Raw -Encoding UTF8
    if ($project -notmatch 'version\s*=\s*"(\d+\.\d+\.\d+)"') {
        throw 'Cannot read version from pyproject.toml'
    }
    $msixVersion = "$($Matches[1]).0"

    Remove-Item $StageDir -Recurse -Force -ErrorAction SilentlyContinue
    $appDir = Join-Path $StageDir 'StructLayoutToolkit'
    New-Item $appDir -ItemType Directory -Force | Out-Null
    Copy-Item "$InputDistPath\*" $appDir -Recurse -Force
    Copy-Item $ManifestPath, 'Square150x150Logo.png', 'Square44x44Logo.png' $StageDir

    $stagedManifest = Join-Path $StageDir 'AppxManifest.xml'
    [xml]$manifest = Get-Content $stagedManifest
    $manifest.Package.Identity.Name = $IdentityName
    $manifest.Package.Identity.Publisher = $Publisher
    $manifest.Package.Identity.Version = $msixVersion
    $manifest.Package.Properties.PublisherDisplayName = $PublisherDisplayName
    $manifest.Save((Resolve-Path $stagedManifest))

    $output = Join-Path $root $OutputMsixPath
    & $MakeAppxPath pack /d (Resolve-Path $StageDir) /p $output /o
    if ($LASTEXITCODE -ne 0) { throw 'makeappx failed' }
}
finally {
    Pop-Location
}