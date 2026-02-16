"""Dataclass models for macOS SDEF (AppleScript dictionary) structures."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Parameter:
    name: str
    type: str = ""
    description: str = ""
    optional: bool = False


@dataclass
class Command:
    name: str
    code: str = ""
    description: str = ""
    direct_parameter: Optional[Parameter] = None
    parameters: List[Parameter] = field(default_factory=list)
    result_type: Optional[str] = None
    result_description: str = ""


@dataclass
class Property:
    name: str
    type: str = ""
    access: str = "rw"
    description: str = ""


@dataclass
class Element:
    type: str
    access: str = ""


@dataclass
class Class:
    name: str
    code: str = ""
    description: str = ""
    inherits: Optional[str] = None
    plural: str = ""
    properties: List[Property] = field(default_factory=list)
    elements: List[Element] = field(default_factory=list)
    responds_to: List[str] = field(default_factory=list)
    is_extension: bool = False
    extends: Optional[str] = None


@dataclass
class EnumValue:
    name: str
    code: str = ""
    description: str = ""


@dataclass
class Enumeration:
    name: str
    code: str = ""
    values: List[EnumValue] = field(default_factory=list)


@dataclass
class Suite:
    name: str
    code: str = ""
    description: str = ""
    commands: List[Command] = field(default_factory=list)
    classes: List[Class] = field(default_factory=list)
    enumerations: List[Enumeration] = field(default_factory=list)


@dataclass
class Dictionary:
    app_name: str
    app_path: str
    suites: List[Suite] = field(default_factory=list)

    def find_command(self, name: str) -> Optional[Command]:
        """Find a command by name across all suites (case-insensitive)."""
        q = name.lower()
        for suite in self.suites:
            for cmd in suite.commands:
                if cmd.name.lower() == q:
                    return cmd
        return None

    def find_class(self, name: str) -> Optional[Class]:
        """Find a class by name across all suites (case-insensitive)."""
        q = name.lower()
        for suite in self.suites:
            for cls in suite.classes:
                if cls.name.lower() == q:
                    return cls
        return None

    def find_enumeration(self, name: str) -> Optional[Enumeration]:
        """Find an enumeration by name across all suites (case-insensitive)."""
        q = name.lower()
        for suite in self.suites:
            for enum in suite.enumerations:
                if enum.name.lower() == q:
                    return enum
        return None

    def find_suite(self, name: str) -> Optional[Suite]:
        """Find a suite by name (case-insensitive)."""
        q = name.lower()
        for suite in self.suites:
            if suite.name.lower() == q:
                return suite
        return None

    def search(self, query: str) -> List[dict]:
        """Search across all names and descriptions. Returns list of
        {"kind": str, "suite": str, "name": str, "description": str}."""
        q = query.lower()
        results = []  # type: List[dict]
        for suite in self.suites:
            if q in suite.name.lower() or q in suite.description.lower():
                results.append({
                    "kind": "suite",
                    "suite": suite.name,
                    "name": suite.name,
                    "description": suite.description,
                })
            for cmd in suite.commands:
                if _matches(q, cmd.name, cmd.description):
                    results.append({
                        "kind": "command",
                        "suite": suite.name,
                        "name": cmd.name,
                        "description": cmd.description,
                    })
            for cls in suite.classes:
                if _matches(q, cls.name, cls.description):
                    results.append({
                        "kind": "class",
                        "suite": suite.name,
                        "name": cls.name,
                        "description": cls.description,
                    })
                for prop in cls.properties:
                    if _matches(q, prop.name, prop.description):
                        results.append({
                            "kind": "property",
                            "suite": suite.name,
                            "name": "%s.%s" % (cls.name, prop.name),
                            "description": prop.description,
                        })
            for enum in suite.enumerations:
                if _matches(q, enum.name):
                    results.append({
                        "kind": "enumeration",
                        "suite": suite.name,
                        "name": enum.name,
                        "description": "",
                    })
                for val in enum.values:
                    if _matches(q, val.name, val.description):
                        results.append({
                            "kind": "enum value",
                            "suite": suite.name,
                            "name": "%s.%s" % (enum.name, val.name),
                            "description": val.description,
                        })
        return results


def _matches(query: str, *fields: str) -> bool:
    for f in fields:
        if query in f.lower():
            return True
    return False
