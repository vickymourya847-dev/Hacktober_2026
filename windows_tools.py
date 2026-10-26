
import os
import shutil
import subprocess
from pathlib import Path


def find_application(name: str):
    """Find an approved Windows application."""

    local = Path(os.environ.get("LOCALAPPDATA", ""))
    program_files = Path(
        os.environ.get("PROGRAMFILES", r"C:\Program Files")
    )
    program_files_x86 = Path(
        os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")
    )

    applications = {
        "chrome": [
            shutil.which("chrome"),
            program_files / "Google/Chrome/Application/chrome.exe",
            program_files_x86 / "Google/Chrome/Application/chrome.exe",
            local / "Google/Chrome/Application/chrome.exe",
        ],
        "vscode": [
            shutil.which("code"),
            local / "Programs/Microsoft VS Code/Code.exe",
            program_files / "Microsoft VS Code/Code.exe",
        ],
        "notepad": [
            shutil.which("notepad"),
            Path(os.environ.get("WINDIR", r"C:\Windows"))
            / "System32/notepad.exe",
        ],
        "calculator": [
            shutil.which("calc"),
            Path(os.environ.get("WINDIR", r"C:\Windows"))
            / "System32/calc.exe",
        ],
    }

    if name not in applications:
        raise ValueError("Application is not on the approved list.")

    for candidate in applications[name]:
        if candidate and Path(candidate).is_file():
            return str(candidate)

    raise FileNotFoundError(
        f"{name} was not found on this computer."
    )


def open_application(name: str):
    name = name.strip().lower()

    executable = find_application(name)

    subprocess.Popen(
        [executable],
        shell=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return {
        "success": True,
        "action": "open_application",
        "application": name,
        "message": f"Launch request sent for {name}."
    }
