"""Tests for the editor launch actions."""

from __future__ import annotations

import sys
from types import SimpleNamespace

import pytest

from struct_layout_toolkit_launcher import app


def test_documents_dir_uses_home_documents_directory(monkeypatch, tmp_path):
    monkeypatch.setattr(app.Path, "home", lambda: tmp_path)
    monkeypatch.delenv("USERPROFILE", raising=False)

    assert app.documents_dir() == tmp_path / "Documents"


def test_application_dir_uses_executable_directory_when_compiled(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setitem(app.__dict__, "__compiled__", True)
    monkeypatch.setattr(app.sys, "executable", str(tmp_path / "application"))

    assert app.application_dir() == tmp_path


@pytest.mark.parametrize("locale_name", ["ja_JP", "Japanese_Japan"])
def test_help_path_uses_system_language(monkeypatch, tmp_path, locale_name):
    help_dir = tmp_path / "help"
    help_dir.mkdir()
    localized_help = help_dir / "help_ja.html"
    localized_help.touch()
    monkeypatch.setattr(app, "application_dir", lambda: tmp_path)
    monkeypatch.setattr(app.locale, "getlocale", lambda: (locale_name, "UTF-8"))

    assert app.help_path() == localized_help


def test_help_path_falls_back_to_english(monkeypatch, tmp_path):
    help_dir = tmp_path / "help"
    help_dir.mkdir()
    english_help = help_dir / "help.html"
    english_help.touch()
    monkeypatch.setattr(app, "application_dir", lambda: tmp_path)
    monkeypatch.setattr(app.locale, "getlocale", lambda: ("fr_FR", "UTF-8"))

    assert app.help_path() == english_help


def test_open_help_uses_default_browser(monkeypatch, tmp_path):
    help_file = tmp_path / "help.html"
    calls = []
    monkeypatch.setattr(app, "help_path", lambda: help_file)
    monkeypatch.setattr(app.webbrowser, "open", calls.append)

    app.open_help()

    assert calls == [help_file.as_uri()]


def test_install_bundled_plugins_preserves_existing_files(
    monkeypatch,
    tmp_path,
):
    bundled_dir = tmp_path / "application" / "plugins"
    bundled_dir.mkdir(parents=True)
    (bundled_dir / "standard.lua").write_text("standard", encoding="utf-8")
    (bundled_dir / "custom.lua").write_text("bundled", encoding="utf-8")
    data_dir = tmp_path / "data"
    plugins_dir = data_dir / "plugins"
    plugins_dir.mkdir(parents=True)
    (plugins_dir / "custom.lua").write_text("user", encoding="utf-8")
    monkeypatch.setattr(app, "application_dir", lambda: bundled_dir.parent)
    monkeypatch.setattr(app, "app_data_dir", lambda: data_dir)

    app.install_bundled_plugins()

    installed = (plugins_dir / "standard.lua").read_text(encoding="utf-8")
    assert installed == "standard"
    assert (plugins_dir / "custom.lua").read_text(encoding="utf-8") == "user"


@pytest.mark.parametrize(
    ("open_editor", "editor_name"),
    [
        (app.open_binary_editor, "binary"),
        (app.open_packet_data_editor, "packet"),
    ],
)
def test_open_editor_starts_separate_process(
    monkeypatch,
    open_editor,
    editor_name,
):
    process = object()
    calls = []
    monkeypatch.setattr(
        app,
        "start_editor_process",
        lambda selected_editor: calls.append(selected_editor) or process,
    )

    result = open_editor(object())

    assert result is process
    assert calls == [editor_name]


def test_editor_command_uses_python_module(monkeypatch):
    monkeypatch.delitem(app.__dict__, "__compiled__", raising=False)
    monkeypatch.setattr(app.sys, "executable", "python")

    assert app.editor_command("binary") == [
        "python",
        "-m",
        "struct_layout_toolkit_launcher",
        "--editor",
        "binary",
    ]


@pytest.mark.skipif(app.os.name != "nt", reason="Windows-specific behavior")
def test_editor_command_uses_pythonw_on_windows(monkeypatch, tmp_path):
    python = tmp_path / "python.exe"
    pythonw = tmp_path / "pythonw.exe"
    pythonw.touch()
    monkeypatch.delitem(app.__dict__, "__compiled__", raising=False)
    monkeypatch.setattr(app.sys, "executable", str(python))

    assert app.editor_command("binary")[0] == str(pythonw)


def test_start_editor_process_detaches_from_launcher(monkeypatch):
    process = object()
    calls = []
    monkeypatch.setattr(app, "editor_command", lambda editor: [editor])
    monkeypatch.setattr(
        app.subprocess,
        "Popen",
        lambda command, **kwargs: calls.append((command, kwargs)) or process,
    )

    result = app.start_editor_process("packet")

    assert result is process
    assert calls[0][0] == ["packet"]
    assert calls[0][1]["close_fds"] is True
    if app.os.name == "nt":
        creationflags = calls[0][1]["creationflags"]
        assert creationflags & app.subprocess.CREATE_NO_WINDOW
        assert not creationflags & app.subprocess.DETACHED_PROCESS
    else:
        assert calls[0][1]["start_new_session"] is True


@pytest.mark.parametrize(
    ("editor_name", "window_name"),
    [
        ("binary", "BinaryEditorWindow"),
        ("packet", "PacketDataEditorWindow"),
    ],
)
def test_run_editor_creates_window_in_child_process(
    monkeypatch,
    tmp_path,
    editor_name,
    window_name,
):
    root = SimpleNamespace(
        withdraw=lambda: None,
        wait_window=lambda window: None,
        destroy=lambda: None,
    )
    window_calls = []

    def fake_window(parent, **kwargs):
        window = object()
        window_calls.append((parent, kwargs, window))
        return window

    sltgui = SimpleNamespace(**{window_name: fake_window})
    monkeypatch.setitem(sys.modules, "sltgui", sltgui)
    monkeypatch.setattr(app.tk, "Tk", lambda: root)
    monkeypatch.setattr(app, "app_data_dir", lambda: tmp_path)
    monkeypatch.setattr(app, "documents_dir", lambda: tmp_path / "Documents")

    app.run_editor(editor_name)

    assert window_calls == [(
        root,
        {
            "apl_dir": tmp_path,
            "data_dir": tmp_path / "Documents",
        },
        window_calls[0][2],
    )]


def test_main_runs_requested_editor_without_launcher(monkeypatch):
    calls = []
    monkeypatch.setattr(app.sys, "argv", ["launcher", "--editor", "packet"])
    monkeypatch.setattr(app, "run_editor", calls.append)
    monkeypatch.setattr(
        app.tk,
        "Tk",
        lambda: pytest.fail("launcher window must not be created"),
    )

    app.main()

    assert calls == ["packet"]
