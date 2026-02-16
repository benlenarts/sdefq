# sdefq

Python 3.9+ CLI and library for querying macOS AppleScript dictionaries (SDEF). Stdlib only, no external deps.

## Structure

- `sdefq/models.py` — dataclasses (Dictionary, Suite, Command, Class, Enumeration, etc.)
- `sdefq/parser.py` — XML → model objects
- `sdefq/resolver.py` — app name → path, list scriptable apps
- `sdefq/formatter.py` — models → human-readable text
- `sdefq/__main__.py` — CLI (argparse)
- `sdefq/__init__.py` — public API: `load()`, `list_apps()`

## Run

```bash
python3 -m sdefq Safari
python3 -m sdefq Safari command "do JavaScript"
```
