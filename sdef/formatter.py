"""Format SDEF model objects as human-readable text."""

from typing import Iterator, List

from .models import Class, Command, Dictionary, Enumeration, Suite


def _desc(description: str) -> str:
    """Return ' — description' or '' if empty."""
    return f" — {description}" if description else ""


def _render(lines: Iterator[str]) -> str:
    """Join yielded lines into a final string."""
    return "\n".join(lines).rstrip() + "\n"


def _format_index_lines(d: Dictionary) -> Iterator[str]:
    suite_word = "suite" if len(d.suites) == 1 else "suites"
    yield f"{d.app_name} — {len(d.suites)} {suite_word}"
    yield ""
    for suite in d.suites:
        yield f"  {suite.name}"
        if suite.description:
            yield f"    {suite.description}"
        cmd_names = ", ".join(c.name for c in suite.commands)
        cls_names = ", ".join(c.name for c in suite.classes)
        enum_names = ", ".join(e.name for e in suite.enumerations)
        yield f"    Commands ({len(suite.commands)}): {cmd_names or '—'}"
        yield f"    Classes  ({len(suite.classes)}): {cls_names or '—'}"
        yield f"    Enums    ({len(suite.enumerations)}): {enum_names or '—'}"
        yield ""


def format_index(d: Dictionary) -> str:
    """Format a dictionary as an index: suites with counts."""
    return _render(_format_index_lines(d))


def _format_suite_lines(suite: Suite) -> Iterator[str]:
    yield suite.name
    if suite.description:
        yield f"  {suite.description}"
    yield ""

    if suite.commands:
        yield "  Commands:"
        for cmd in suite.commands:
            yield f"    {cmd.name}"
            if cmd.description:
                yield f"      {cmd.description}"
    yield ""

    if suite.classes:
        yield "  Classes:"
        for cls in suite.classes:
            label = f"{cls.name} (extension)" if cls.is_extension else cls.name
            yield f"    {label}"
            if cls.description:
                yield f"      {cls.description}"
    yield ""

    if suite.enumerations:
        yield "  Enumerations:"
        for enum in suite.enumerations:
            val_names = ", ".join(v.name for v in enum.values)
            yield f"    {enum.name}: {val_names}"
    yield ""


def format_suite(suite: Suite) -> str:
    """Format a full suite with all its contents."""
    return _render(_format_suite_lines(suite))


def _format_command_lines(cmd: Command, suite_name: str) -> Iterator[str]:
    header = f"command: {cmd.name}"
    if suite_name:
        header += f" (suite: {suite_name})"
    yield header
    if cmd.description:
        yield f"  {cmd.description}"

    if cmd.direct_parameter:
        dp = cmd.direct_parameter
        opt = "optional" if dp.optional else "required"
        yield f"  Direct parameter: {dp.type} ({opt})"
        if dp.description and dp.description != dp.type:
            yield f"    {dp.description}"

    if cmd.parameters:
        yield "  Parameters:"
        for p in cmd.parameters:
            opt = "optional" if p.optional else "required"
            yield f"    {p.name}  {p.type}  ({opt}){_desc(p.description)}"

    if cmd.result_type:
        yield f"  Returns: {cmd.result_type}{_desc(cmd.result_description)}"


def format_command(cmd: Command, suite_name: str = "") -> str:
    """Format a single command with full detail."""
    return _render(_format_command_lines(cmd, suite_name))


def _format_class_lines(cls: Class, suite_name: str) -> Iterator[str]:
    kind = "class extension" if cls.is_extension else "class"
    header = f"{kind}: {cls.name}"
    if suite_name:
        header += f" (suite: {suite_name})"
    yield header
    if cls.description:
        yield f"  {cls.description}"
    if cls.inherits:
        yield f"  Inherits from: {cls.inherits}"

    if cls.properties:
        yield "  Properties:"
        for p in cls.properties:
            access = p.access if p.access else "rw"
            yield f"    {p.name:<20s} {p.type:<12s} ({access}){_desc(p.description)}"

    if cls.elements:
        yield "  Elements:"
        for e in cls.elements:
            yield f"    {e.type}"

    if cls.responds_to:
        yield f"  Responds to: {', '.join(cls.responds_to)}"


def format_class(cls: Class, suite_name: str = "") -> str:
    """Format a single class with full detail."""
    return _render(_format_class_lines(cls, suite_name))


def _format_enumeration_lines(enum: Enumeration, suite_name: str) -> Iterator[str]:
    header = f"enum: {enum.name}"
    if suite_name:
        header += f" (suite: {suite_name})"
    yield header
    for v in enum.values:
        yield f"  {v.name}{_desc(v.description)}"


def format_enumeration(enum: Enumeration, suite_name: str = "") -> str:
    """Format a single enumeration with all values."""
    return _render(_format_enumeration_lines(enum, suite_name))


def format_search_results(results: List[dict]) -> str:
    """Format search results."""
    if not results:
        return "No matches found.\n"
    return _render(
        line
        for r in results
        for line in (
            f"  [{r['kind']}] {r['name']}{_desc(r['description'])}",
            f"    in {r['suite']}",
        )
    )


def format_command_list(commands: List[Command]) -> str:
    """Format a list of all commands with brief descriptions."""
    if not commands:
        return "No commands found.\n"
    return _render(f"  {cmd.name}{_desc(cmd.description)}" for cmd in commands)


def format_class_list(classes: List[Class]) -> str:
    """Format a list of all classes with brief descriptions."""
    if not classes:
        return "No classes found.\n"
    return _render(f"  {cls.name}{_desc(cls.description)}" for cls in classes)


def format_enumeration_list(enums: List[Enumeration]) -> str:
    """Format a list of all enumerations."""
    if not enums:
        return "No enumerations found.\n"
    return _render(
        f"  {enum.name}: {', '.join(v.name for v in enum.values)}" for enum in enums
    )


def format_app_list(apps: List[tuple]) -> str:
    """Format the list of scriptable apps."""
    if not apps:
        return "No scriptable apps found.\n"
    return _render(f"  {name:<30s} {path}" for name, path in apps)
