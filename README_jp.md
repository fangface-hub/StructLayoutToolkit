# StructLayoutToolkit

`sltgui>=1.0.1` が提供する次の GUI を起動するデスクトップランチャーです。

- Binary Editor (`BinaryEditorWindow`)
- Packet Data Editor (`PacketDataEditorWindow`)

## Requirements

- Python 3.14 以降（Tkinter を含むこと）
- [uv](https://docs.astral.sh/uv/)
- PowerShell 7（配布スクリプトを使う場合）

Linux では Tkinter の OS パッケージも必要です。Ubuntu の場合は
`sudo apt-get install python3-tk` でインストールできます。

## Development

```powershell
uv sync --group dev
uv run struct-layout-toolkit
uv run pytest
```

依存関係は `uv.lock` に固定されます。更新時は `uv lock --upgrade` を実行してください。

## Build

Windows、macOS、Linux の standalone onefolder アプリを作成します。

```powershell
./build_nuitka.ps1
```

Windows で MSIX を作成する場合は Windows SDK の `makeappx.exe` が必要です。

```powershell
./build_msix.ps1 -Publisher "CN=<publisher ID>" -IdentityName "<identity>" -PublisherDisplayName "<publisher>"
```

Microsoft Store へ提出する MSIX は Store 側で署名されるため、CI は未署名の
`.msix` を成果物として生成します。Identity と Publisher は Partner Center の
「製品 ID」ページに表示される値と完全に一致させてください。

## Release

`.github/workflows` の各 workflow は手動実行できます。`bump_major.ps1`、
`bump_minor.ps1`、`bump_patch.ps1` は `pyproject.toml`、パッケージ内の
バージョン、MSIX マニフェストを同時に更新します。
