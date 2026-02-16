"""CLI entry point for sdefq. Run with: python -m sdef"""

import argparse
import sys

import sdef
from sdef.formatter import (
    format_app_list,
    format_class,
    format_command,
    format_enumeration,
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
            sys.stderr.write("Error: specify a command name.\n")
            sys.exit(1)
        cmd = d.find_command(args.name)
        if not cmd:
            sys.stderr.write("Command '%s' not found.\n" % args.name)
            sys.exit(1)
        sys.stdout.write(format_command(cmd))
        return

    if args.scope == "class":
        if not args.name:
            sys.stderr.write("Error: specify a class name.\n")
            sys.exit(1)
        cls = d.find_class(args.name)
        if not cls:
            sys.stderr.write("Class '%s' not found.\n" % args.name)
            sys.exit(1)
        sys.stdout.write(format_class(cls))
        return

    if args.scope in ("enum", "enumeration"):
        if not args.name:
            sys.stderr.write("Error: specify an enumeration name.\n")
            sys.exit(1)
        enum = d.find_enumeration(args.name)
        if not enum:
            sys.stderr.write("Enumeration '%s' not found.\n" % args.name)
            sys.exit(1)
        sys.stdout.write(format_enumeration(enum))
        return

    # Otherwise, scope is a suite name
    suite = d.find_suite(args.scope)
    if not suite:
        sys.stderr.write("Suite '%s' not found.\n" % args.scope)
        sys.exit(1)
    sys.stdout.write(format_suite(suite))


if __name__ == "__main__":
    main()
