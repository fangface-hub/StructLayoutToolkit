# StructLayoutToolkit

A desktop launcher for the following GUIs provided by `sltgui>=1.0.1`:

- Binary Editor (`BinaryEditorWindow`)
- Packet Data Editor (`PacketDataEditorWindow`)

## Requirements

- Python 3.14 or later (including Tkinter)
- [uv](https://docs.astral.sh/uv/)
- PowerShell 7 (when using the distribution scripts)

Linux also requires the Tkinter OS package. On Ubuntu, install it with
`sudo apt-get install python3-tk`.

## Development

```powershell
uv sync --group dev
uv run struct-layout-toolkit
uv run pytest
```

Dependencies are locked in `uv.lock`. Run `uv lock --upgrade` to update them.

## Build

Build standalone onefolder applications for Windows, macOS, and Linux:

```powershell
./build_nuitka.ps1
```

Building an MSIX package on Windows requires `makeappx.exe` from the Windows SDK.

```powershell
./build_msix.ps1 -Publisher "CN=<publisher ID>" -IdentityName "<identity>" -PublisherDisplayName "<publisher>"
```

Because Microsoft Store signs submitted MSIX packages, CI produces an unsigned
`.msix` artifact. The Identity and Publisher values must exactly match those shown
on the Product identity page in Partner Center.

## Release

Each workflow in `.github/workflows` can be run manually. The `bump_major.ps1`,
`bump_minor.ps1`, and `bump_patch.ps1` scripts update `pyproject.toml`, the package
version, and the MSIX manifest together.
