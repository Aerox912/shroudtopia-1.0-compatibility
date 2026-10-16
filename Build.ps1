$ErrorActionPreference = 'Stop'
$msbuild = (Get-Command MSBuild.exe -ErrorAction Stop).Source
$source = (Resolve-Path (Join-Path $PSScriptRoot 'snapshot\shroudtopia')).Path + '\'
foreach ($name in @('shroudtopia','winmm')) {
    $project = Join-Path $source "$name\$name.vcxproj"
    $out = Join-Path $PSScriptRoot "build\$name\"
    $obj = Join-Path $PSScriptRoot "build\obj-$name\"
    & $msbuild $project /p:Configuration=Release /p:Platform=x64 /p:PlatformToolset=v143 "/p:SolutionDir=$source" "/p:OutDir=$out" "/p:IntDir=$obj" /nologo /v:minimal
    if ($LASTEXITCODE -ne 0) { throw "Build failed: $name" }
}
