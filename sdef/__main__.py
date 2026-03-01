"""CLI entry point for sdefq. Run with: python -m sdef"""

import argparse
import os
import pkgutil
import sys

import sdef
from sdef.formatter import (
    format_app_list,
    format_class,
    format_class_list,
    format_command,
    format_command_list,
    format_enumeration,
    format_enumeration_list,
    format_index,
    format_search_results,
    format_suite,
)


def main():
    parser = argparse.ArgumentParser(
        prog="sdefq",
        description="Query macOS AppleScript dictionaries (SDEF).",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all scriptable applications.",
    )
    parser.add_argument(
        "--skill", action="store_true",
        help="Print the Claude Code skill file to stdout.",
    )
    parser.add_argument(
        "--install-skill-into", metavar="DIR",
        help="Install the skill file to DIR/sdefq/SKILL.md.",
    )
    parser.add_argument(
        "app", nargs="?",
        help="App name (e.g. Safari) or path (/Applications/Safari.app/).",
    )
    parser.add_argument(
        "scope", nargs="?",
        help='Scope: suite name, or one of "command", "class", "enum".',
    )
    parser.add_argument(
        "name", nargs="?",
        help="Name of the command, class, or enumeration to look up.",
    )
    parser.add_argument(
        "--search", "-s", metavar="QUERY",
        help="Search across the app's entire dictionary.",
    )

    args = parser.parse_args()

    if args.install_skill_into:
        data = pkgutil.get_data("sdef", "skill.md")
        dest_dir = os.path.join(os.path.expanduser(args.install_skill_into), "sdefq")
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "SKILL.md")
        with open(dest, "wb") as f:
            f.write(data)
        sys.stderr.write("Installed %s\n" % dest)
        return

    if args.skill:
        data = pkgutil.get_data("sdef", "skill.md")
        sys.stdout.buffer.write(data)
        return

    if args.list:
        apps = sdef.list_apps()
        sys.stdout.write(format_app_list(apps))
        return

    if not args.app:
        parser.print_help()
        sys.exit(1)

    try:
        d = sdef.load(args.app)
    except FileNotFoundError as e:
        sys.stderr.write("Error: %s\n" % e)
        sys.exit(1)
    except RuntimeError as e:
        sys.stderr.write("Error: %s\n" % e)
        sys.exit(1)
    except ValueError as e:
        sys.stderr.write("Error: %s\n" % e)
        sys.exit(1)

    # Search mode
    if args.search:
        results = d.search(args.search)
        sys.stdout.write(format_search_results(results))
        return

    # No scope → index
    if not args.scope:
        sys.stdout.write(format_index(d))
        return

    # Scope is "command", "class", or "enum" → lookup by name
    if args.scope in ("command", "cmd"):
        if not args.name:
            cmds = [c for s in d.suites for c in s.commands]
            sys.stdout.write(format_command_list(cmds))
            return
        cmd, suite_name = d.find_command(args.name)
        if not cmd:
            sys.stderr.write("Command '%s' not found.\n" % args.name)
            sys.exit(1)
        sys.stdout.write(format_command(cmd, suite_name))
        return

    if args.scope == "class":
        if not args.name:
            classes = [c for s in d.suites for c in s.classes]
            sys.stdout.write(format_class_list(classes))
            return
        cls, suite_name = d.find_class(args.name)
        if not cls:
            sys.stderr.write("Class '%s' not found.\n" % args.name)
            sys.exit(1)
        sys.stdout.write(format_class(cls, suite_name))
        return

    if args.scope in ("enum", "enumeration"):
        if not args.name:
            enums = [e for s in d.suites for e in s.enumerations]
            sys.stdout.write(format_enumeration_list(enums))
            return
        enum, suite_name = d.find_enumeration(args.name)
        if not enum:
            sys.stderr.write("Enumeration '%s' not found.\n" % args.name)
            sys.exit(1)
        sys.stdout.write(format_enumeration(enum, suite_name))
        return

    # Otherwise, scope is a suite name
    suite = d.find_suite(args.scope)
    if not suite:
        sys.stderr.write("Suite '%s' not found.\n" % args.scope)
        sys.exit(1)
    sys.stdout.write(format_suite(suite))


if __name__ == "__main__":
    main()
