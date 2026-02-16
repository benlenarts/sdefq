# sdefq

Python 3.9+ CLI and library for querying macOS AppleScript dictionaries (SDEF). Stdlib only, no external deps.

## Structure

- `sdef/` — library package (`import sdef`)
  - `models.py` — dataclasses (Dictionary, Suite, Command, Class, Enumeration, etc.)
  - `parser.py` — XML → model objects
  - `resolver.py` — app name → path, list scriptable apps
  - `formatter.py` — models → human-readable text
  - `__main__.py` — CLI entry point (argparse)
  - `__init__.py` — public API: `load()`, `list_apps()`
  - `skill.md` — Claude Code skill (printed by `--skill`)
- `bin/sdefq` — executable CLI wrapper

## Run

```bash
bin/sdefq Safari
bin/sdefq Safari command "do JavaScript"
bin/sdefq --install-skill-into ~/.claude/skills
```
