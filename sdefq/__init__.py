"""sdefq — query macOS AppleScript dictionaries (SDEF)."""

from .models import (
    Class,
    Command,
    Dictionary,
    Element,
    EnumValue,
    Enumeration,
    Parameter,
    Property,
    Suite,
)
from .parser import parse_xml
from .resolver import app_name_from_path, get_sdef_xml, list_scriptable_apps, resolve_app

__all__ = [
    "load",
    "list_apps",
    "Dictionary",
    "Suite",
    "Command",
    "Class",
    "Property",
    "Element",
    "Enumeration",
    "EnumValue",
    "Parameter",
]


def load(app: str) -> Dictionary:
    """Load and parse the SDEF for an app.

    Args:
        app: App name ("Safari") or path ("/Applications/Safari.app/").

    Returns:
        A Dictionary object with all suites, commands, classes, and enums.
    """
    app_path = resolve_app(app)
    xml_bytes = get_sdef_xml(app_path)
    name = app_name_from_path(app_path)
    return parse_xml(xml_bytes, app_name=name, app_path=app_path)


def list_apps():
    """List all scriptable apps. Returns list of (name, path) tuples."""
    return list_scriptable_apps()
