"""Format SDEF model objects as human-readable text."""

from typing import List

from .models import Class, Command, Dictionary, Enumeration, Suite


def format_index(d: Dictionary) -> str:
    """Format a dictionary as an index: suites with counts."""
    lines = []  # type: List[str]
    suite_word = "suite" if len(d.suites) == 1 else "suites"
    lines.append("%s — %d %s" % (d.app_name, len(d.suites), suite_word))
    lines.append("")
    for suite in d.suites:
        lines.append("  %s" % suite.name)
        if suite.description:
            lines.append("    %s" % suite.description)
        cmd_names = ", ".join(c.name for c in suite.commands)
        cls_names = ", ".join(c.name for c in suite.classes)
        enum_names = ", ".join(e.name for e in suite.enumerations)
        lines.append("    Commands (%d): %s" % (len(suite.commands), cmd_names or "—"))
        lines.append("    Classes  (%d): %s" % (len(suite.classes), cls_names or "—"))
        lines.append("    Enums    (%d): %s" % (len(suite.enumerations), enum_names or "—"))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def format_suite(suite: Suite) -> str:
    """Format a full suite with all its contents."""
    lines = []  # type: List[str]
    lines.append(suite.name)
    if suite.description:
        lines.append("  %s" % suite.description)
    lines.append("")

    if suite.commands:
        lines.append("  Commands:")
        for cmd in suite.commands:
            lines.append("    %s" % cmd.name)
            if cmd.description:
                lines.append("      %s" % cmd.description)
    lines.append("")

    if suite.classes:
        lines.append("  Classes:")
        for cls in suite.classes:
            label = cls.name
            if cls.is_extension:
                label = "%s (extension)" % cls.name
            lines.append("    %s" % label)
            if cls.description:
                lines.append("      %s" % cls.description)
    lines.append("")

    if suite.enumerations:
        lines.append("  Enumerations:")
        for enum in suite.enumerations:
            val_names = ", ".join(v.name for v in enum.values)
            lines.append("    %s: %s" % (enum.name, val_names))
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def format_command(cmd: Command) -> str:
    """Format a single command with full detail."""
    lines = []  # type: List[str]
    lines.append(cmd.name)
    if cmd.description:
        lines.append("  %s" % cmd.description)

    if cmd.direct_parameter:
        dp = cmd.direct_parameter
        opt = "optional" if dp.optional else "required"
        lines.append("  Direct parameter: %s (%s)" % (dp.type, opt))
        if dp.description and dp.description != dp.type:
            lines.append("    %s" % dp.description)

    if cmd.parameters:
        lines.append("  Parameters:")
        for p in cmd.parameters:
            opt = "optional" if p.optional else "required"
            desc = ""
            if p.description:
                desc = " — %s" % p.description
            lines.append("    %s  %s  (%s)%s" % (p.name, p.type, opt, desc))

    if cmd.result_type:
        desc = ""
        if cmd.result_description:
            desc = " — %s" % cmd.result_description
        lines.append("  Returns: %s%s" % (cmd.result_type, desc))

    return "\n".join(lines) + "\n"


def format_class(cls: Class) -> str:
    """Format a single class with full detail."""
    lines = []  # type: List[str]
    label = cls.name
    if cls.is_extension:
        label = "%s (class extension)" % cls.name
    lines.append(label)
    if cls.description:
        lines.append("  %s" % cls.description)
    if cls.inherits:
        lines.append("  Inherits from: %s" % cls.inherits)

    if cls.properties:
        lines.append("  Properties:")
        for p in cls.properties:
            access = p.access if p.access else "rw"
            desc = ""
            if p.description:
                desc = " — %s" % p.description
            lines.append("    %-20s %-12s (%s)%s" % (p.name, p.type, access, desc))

    if cls.elements:
        lines.append("  Elements:")
        for e in cls.elements:
            lines.append("    %s" % e.type)

    if cls.responds_to:
        lines.append("  Responds to: %s" % ", ".join(cls.responds_to))

    return "\n".join(lines) + "\n"


def format_enumeration(enum: Enumeration) -> str:
    """Format a single enumeration with all values."""
    lines = []  # type: List[str]
    lines.append(enum.name)
    for v in enum.values:
        desc = ""
        if v.description:
            desc = " — %s" % v.description
        lines.append("  %s%s" % (v.name, desc))
    return "\n".join(lines) + "\n"


def format_search_results(results: List[dict]) -> str:
    """Format search results."""
    if not results:
        return "No matches found.\n"
    lines = []  # type: List[str]
    for r in results:
        desc = ""
        if r["description"]:
            desc = " — %s" % r["description"]
        lines.append("  [%s] %s%s" % (r["kind"], r["name"], desc))
        lines.append("    in %s" % r["suite"])
    return "\n".join(lines) + "\n"


def format_app_list(apps: List[tuple]) -> str:
    """Format the list of scriptable apps."""
    if not apps:
        return "No scriptable apps found.\n"
    lines = []  # type: List[str]
    for name, path in apps:
        lines.append("  %-30s %s" % (name, path))
    return "\n".join(lines) + "\n"
