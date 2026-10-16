# Shroudtopia: Enshrouded 1.0 compatibility source

Exact source for Nexus mod 143, optional file 833, version 1.0-r1:
[Shroudtopia - Enshrouded 1.0 compatibility](https://www.nexusmods.com/enshrouded/mods/143?tab=files).

SOURCE.zip is copied unchanged from that upload. The snapshot/ directory is its byte-for-byte extraction, including original notices and verification helpers. No fixes or newer development changes have been mixed into this review snapshot. Documentation and build helpers at repository root are added for reviewers.

Original Shroudtopia and WINMM proxy: [s0T7x / Miguel Oppermann](https://github.com/s0t7x/shroudtopia), MIT license. Recorded upstream baseline: 195e6189e7e695a06f5cb4ca6830c0b08cc3ac8f. Compatibility maintenance: Aerox912.

## Build on Windows

Install Visual Studio 2022 Build Tools with Desktop development with C++, MSVC v143 x64 tools and a Windows 10/11 SDK. In Developer PowerShell, run:

    .\Build.ps1

The script builds only the two Release x64 DLL projects into build/. It does not start the game or install anything. The required nlohmann JSON headers are included. Debug configurations reference additional libraries and are outside these instructions.

Equivalent MSBuild commands, from the repository root:

    $root = (Resolve-Path .\snapshot\shroudtopia).Path + '\'
    msbuild .\snapshot\shroudtopia\shroudtopia\shroudtopia.vcxproj /p:Configuration=Release /p:Platform=x64 /p:PlatformToolset=v143 "/p:SolutionDir=$root"
    msbuild .\snapshot\shroudtopia\winmm\winmm.vcxproj /p:Configuration=Release /p:Platform=x64 /p:PlatformToolset=v143 "/p:SolutionDir=$root"

Compiler/SDK versions, timestamps and build paths can affect binary hashes. Source identity is verified separately; bit-for-bit rebuilt DLL identity is not claimed.

## Review identity

- Nexus archive: 10319eb8094a9ebff33c7a0078e39a59e46a28a85642867d6e26d6ea5bc51df9
- SOURCE.zip: 423cbb41b5865e4aaba3ea81836114cb9fe8e147d6b347bd0e6baeccea261665
- Uploaded shroudtopia.dll: 1bdf2b961180faddf06ad55fc86347e36b8f44e70cc20d305de6fa36050a6bcb
- Uploaded winmm.dll: dff3845c834912a540f5f63752a5e357049eab7279abd330ca24dc571905cd52
- Target client: Steam build 25966634, EXE SHA-256 4d6d43ea4a91e71c82d60b045dde932179c99e32e40657efe374688b2933589a

The proxy loads the Shroudtopia loader and forwards WINMM calls to Windows. The loader loads configured native mods. The source includes regression/probe helpers; some retain original local analysis paths and require adaptation. They do not constitute a malware audit.

The Nexus archive is quarantined pending staff review. Its notice lists generic possible triggers; no exact detection has been supplied. This source publication is for transparent review, not a claim of security clearance.

Build verification: both Release x64 DLL projects compiled successfully on 16 October 2026 using Visual Studio 2022 Build Tools. Existing compiler warnings remain in this unchanged snapshot. All 74 extracted source files were checked byte-for-byte against SOURCE.zip. This is build and provenance verification, not a security audit.
