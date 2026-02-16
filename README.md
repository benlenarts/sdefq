# sdefq

Query macOS AppleScript dictionaries (SDEF) from the command line or Python.

Built on the system `/usr/bin/sdef` tool. No external dependencies — Python 3.9+ stdlib only.

## CLI Usage

```bash
# List all scriptable apps
python3 -m sdefq --list

# App index — suites with command/class/enum counts
python3 -m sdefq Safari
python3 -m sdefq /Applications/Safari.app/

# Suite detail — all commands, classes, enums
python3 -m sdefq Safari "Safari suite"

# Command detail — parameters, types, return value
python3 -m sdefq Safari command "do JavaScript"

# Class detail — properties, elements, responds-to
python3 -m sdefq Safari class tab

# Enumeration — all values
python3 -m sdefq Keynote enum "export format"

# Search across an app's entire dictionary
python3 -m sdefq Safari --search JavaScript
```

## Python API

```python
import sdefq

# Load an app's dictionary
d = sdefq.load("Safari")

# Browse suites
for suite in d.suites:
    print(suite.name, len(suite.commands), "commands")

# Look up specific items
cmd = d.find_command("do JavaScript")
cls = d.find_class("tab")
enum = d.find_enumeration("export format")

# Search
results = d.search("JavaScript")

# List scriptable apps
apps = sdefq.list_apps()  # [(name, path), ...]
```

## Models

- `Dictionary` — top level, contains suites
- `Suite` — contains commands, classes, enumerations
- `Command` — name, parameters, return type
- `Class` — properties, elements, responds-to, inheritance
- `Enumeration` — list of named values
- `Property`, `Element`, `Parameter`, `EnumValue` — leaf types
