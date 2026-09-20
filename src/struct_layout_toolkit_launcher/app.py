"""Desktop launcher for the editors provided by sltgui."""

from __future__ import annotations

import argparse
import locale
import os
import shutil
import subprocess
import sys
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import ttk
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from collections.abc import Callable

APP_NAME = "StructLayoutToolkit"
EditorName = Literal["binary", "packet"]
LOCALE_LANGUAGE_CODES = {
    "japanese": "ja",
}


def app_data_dir() -> Path:
    """Return a writable, platform-appropriate application data directory."""
    if os.name == "nt":
        fallback = Path.home() / "AppData" / "Local"
        base_dir = Path(os.environ.get("LOCALAPPDATA", fallback))
    elif os.name == "posix" and "darwin" in os.sys.platform:
        base_dir = Path.home() / "Library" / "Application Support"
    else:
        fallback = Path.home() / ".config"
        base_dir = Path(os.environ.get("XDG_CONFIG_HOME", fallback))
    return base_dir / APP_NAME


def documents_dir() -> Path:
    """Return the platform-appropriate Documents directory."""
    if os.name == "nt":
        home_dir = Path(os.environ.get("USERPROFILE", Path.home()))
    else:
        home_dir = Path.home()
    return home_dir / "Documents"


def application_dir() -> Path:
    """Return the directory containing application resources."""
    if "__compiled__" in globals():
        return Path(sys.executable).parent
    return Path(__file__).resolve().parents[2]


def help_path() -> Path:
    """Return localized help when available, otherwise English help."""
    help_dir = application_dir() / "help"
    locale_name = locale.getlocale()[0]
    if locale_name:
        language = locale_name.replace("-", "_").split("_", 1)[0].lower()
        language = LOCALE_LANGUAGE_CODES.get(language, language)
        localized_help = help_dir / f"help_{language}.html"
        if localized_help.is_file():
            return localized_help
    return help_dir / "help.html"


def open_help() -> None:
    """Open the user guide in the default browser."""
    webbrowser.open(help_path().as_uri())


def install_bundled_plugins() -> None:
    """Install missing bundled plugins without overwriting user files."""
    bundled_dir = application_dir() / "plugins"
    if not bundled_dir.is_dir():
        return
    plugins_dir = app_data_dir() / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    for source_path in bundled_dir.glob("*.lua"):
        destination_path = plugins_dir / source_path.name
        if not destination_path.exists():
            shutil.copy2(source_path, destination_path)


def editor_command(editor_name: EditorName) -> list[str]:
    """Return the command used to start an editor process."""
    editor_args = ["--editor", editor_name]
    if "__compiled__" in globals():
        return [sys.executable, *editor_args]

    executable = Path(sys.executable)
    if os.name == "nt":
        pythonw = executable.with_name("pythonw.exe")
        if pythonw.is_file():
            executable = pythonw
    return [
        str(executable),
        "-m",
        "struct_layout_toolkit_launcher",
        *editor_args,
    ]


def start_editor_process(editor_name: EditorName) -> subprocess.Popen[bytes]:
    """Start an editor independently from the launcher process."""
    if os.name == "nt":
        creationflags = (subprocess.CREATE_NEW_PROCESS_GROUP
                         | subprocess.CREATE_NO_WINDOW)
        return subprocess.Popen(
            editor_command(editor_name),
            close_fds=True,
            creationflags=creationflags,
        )
    return subprocess.Popen(
        editor_command(editor_name),
        close_fds=True,
        start_new_session=True,
    )


def open_binary_editor(_parent: tk.Misc) -> subprocess.Popen[bytes]:
    """Open sltgui's binary editor in a separate process."""
    return start_editor_process("binary")


def open_packet_data_editor(_parent: tk.Misc) -> subprocess.Popen[bytes]:
    """Open sltgui's reassembled packet data editor in a separate process."""
    return start_editor_process("packet")


def run_editor(editor_name: EditorName) -> None:
    """Run one editor in the current child process."""
    install_bundled_plugins()
    root = tk.Tk()
    root.withdraw()

    if editor_name == "binary":
        from sltgui import BinaryEditorWindow

        window_class = BinaryEditorWindow
    else:
        from sltgui import PacketDataEditorWindow

        window_class = PacketDataEditorWindow
    window = window_class(
        root,
        apl_dir=app_data_dir(),
        data_dir=documents_dir(),
    )
    try:
        root.wait_window(window)
    finally:
        root.destroy()


def create_launcher(root: tk.Tk) -> ttk.Frame:
    """Populate the root window with editor launch actions."""
    root.title(APP_NAME)
    root.geometry("440x290")
    root.minsize(400, 270)

    frame = ttk.Frame(root, padding=24)
    frame.pack(fill=tk.BOTH, expand=True)
    heading = ttk.Label(
        frame,
        text=APP_NAME,
        font=("TkDefaultFont", 18, "bold"),
    )
    heading.pack(pady=(4, 22))

    actions: tuple[tuple[str, Callable[[tk.Misc], subprocess.Popen[bytes]]],
                   ...] = (
                       ("Binary Editor", open_binary_editor),
                       ("Packet Data Editor", open_packet_data_editor),
                   )
    for label, command in actions:
        button = ttk.Button(
            frame,
            text=label,
            command=lambda action=command: action(root),
        )
        button.pack(fill=tk.X, pady=6, ipady=8)
    ttk.Button(frame, text="Help", command=open_help).pack(
        fill=tk.X,
        pady=(18, 6),
        ipady=8,
    )
    return frame


def main() -> None:
    """Start the launcher application."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--editor", choices=("binary", "packet"))
    args = parser.parse_args()
    if args.editor is not None:
        run_editor(args.editor)
        return

    root = tk.Tk()
    create_launcher(root)
    root.mainloop()
