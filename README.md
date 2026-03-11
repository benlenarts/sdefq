# sdefq

Query macOS AppleScript dictionaries (SDEF) from the command line or Python.

Built on the system `/usr/bin/sdef` tool. No external dependencies — Python 3.9+ stdlib only.

## Install

```bash
brew tap benlenarts/tap
brew install sdefq
```

Or run directly from the repo with `bin/sdefq` or `python3 -m sdef`.

## CLI Usage

```bash
# List all scriptable apps
sdefq --list

# App index — suites with command/class/enum counts
sdefq Safari
sdefq /Applications/Safari.app/

# Suite detail — all commands, classes, enums
sdefq Safari "Safari suite"

# Command detail — parameters, types, return value
sdefq Safari command "do JavaScript"

# Class detail — properties, elements, responds-to
sdefq Safari class tab

# Enumeration — all values
sdefq Keynote enum "export format"

# Search across an app's entire dictionary
sdefq Safari --search JavaScript
```

### Claude Code plugin

sdefq includes a Claude Code plugin that teaches Claude how to query AppleScript dictionaries when writing automation scripts.

```bash
# Load during development
claude --plugin-dir /path/to/sdefq

# Install as a user plugin
claude plugin install --plugin-dir /path/to/sdefq
```

## Python API

```python
import sdef

# Load an app's dictionary
d = sdef.load("Safari")

# Browse suites
for suite in d.suites:
    print(suite.name, len(suite.commands), "commands")

# Look up specific items — returns (object, suite_name) tuples
cmd, suite = d.find_command("do JavaScript")
cls, suite = d.find_class("tab")
enum, suite = d.find_enumeration("export format")

# Search
results = d.search("JavaScript")

# List scriptable apps
apps = sdef.list_apps()  # [(name, path), ...]
```

## Models

- `Dictionary` — top level, contains suites
- `Suite` — contains commands, classes, enumerations
- `Command` — name, parameters, return type
- `Class` — properties, elements, responds-to, inheritance
- `Enumeration` — list of named values
- `Property`, `Element`, `Parameter`, `EnumValue` — leaf types
