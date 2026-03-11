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
- `skills/applescript-discovery/SKILL.md` — Claude Code plugin skill
- `.claude-plugin/plugin.json` — Claude Code plugin manifest
- `bin/sdefq` — executable CLI wrapper

## Run

```bash
bin/sdefq Safari
bin/sdefq Safari command "do JavaScript"
claude plugin install --plugin-dir .
```
