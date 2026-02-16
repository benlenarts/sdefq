"""Resolve app names to paths and discover scriptable applications."""

import os
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple


# Directories to search for .app bundles
APP_DIRS = [
    "/Applications",
    "/System/Applications",
    os.path.expanduser("~/Applications"),
    "/Applications/Utilities",
    "/System/Applications/Utilities",
]


def resolve_app(name_or_path: str) -> str:
    """Resolve an app name or path to a full .app bundle path.

    Accepts:
      - Full path: /Applications/Safari.app or /Applications/Safari.app/
      - App name: Safari, "Google Chrome"

    Returns the resolved path. Raises FileNotFoundError if not found.
    """
    # If it looks like a path (contains / or ends with .app)
    if "/" in name_or_path or name_or_path.endswith(".app"):
        path = name_or_path.rstrip("/")
        if not path.endswith(".app"):
            # Maybe they gave a directory containing an .app
            path = path
        if os.path.isdir(path):
            return path
        raise FileNotFoundError("App not found: %s" % name_or_path)

    # Search by name
    for app_dir in APP_DIRS:
        candidate = os.path.join(app_dir, name_or_path + ".app")
        if os.path.isdir(candidate):
            return candidate

    raise FileNotFoundError(
        "App '%s' not found. Searched: %s" % (name_or_path, ", ".join(APP_DIRS))
    )


def get_sdef_xml(app_path: str) -> bytes:
    """Get raw SDEF XML for an app by calling /usr/bin/sdef."""
    result = subprocess.run(
        ["/usr/bin/sdef", app_path],
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError("sdef failed for %s: %s" % (app_path, stderr))
    return result.stdout


def app_name_from_path(app_path: str) -> str:
    """Extract app name from bundle path: /Applications/Safari.app → Safari."""
    return Path(app_path).stem


def list_scriptable_apps() -> List[Tuple[str, str]]:
    """Find apps that have SDEF scripting dictionaries.

    Returns list of (app_name, app_path) sorted by name.
    """
    apps = []  # type: List[Tuple[str, str]]
    seen = set()  # type: set

    for app_dir in APP_DIRS:
        if not os.path.isdir(app_dir):
            continue
        for entry in _list_app_bundles(app_dir):
            app_path = os.path.join(app_dir, entry)
            if app_path in seen:
                continue
            seen.add(app_path)
            if _has_sdef(app_path):
                name = Path(entry).stem
                apps.append((name, app_path))

    apps.sort(key=lambda x: x[0].lower())
    return apps


def _list_app_bundles(directory: str) -> List[str]:
    """List .app entries in a directory."""
    try:
        return [e for e in os.listdir(directory) if e.endswith(".app")]
    except OSError:
        return []


def _has_sdef(app_path: str) -> bool:
    """Check if an app bundle contains a scripting dictionary."""
    resources = os.path.join(app_path, "Contents", "Resources")
    if os.path.isdir(resources):
        try:
            for f in os.listdir(resources):
                if f.endswith(".sdef"):
                    return True
        except OSError:
            pass
    # Also check for aete-based scriptability via the sdef command
    # (some apps use older formats). We skip this for speed in listing.
    return False
