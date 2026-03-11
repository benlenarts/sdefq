---
name: applescript-discovery
description: Query macOS AppleScript dictionaries (SDEF) to look up commands, classes, properties, and enumerations for scriptable applications. Use when writing AppleScript or JXA automation, or when the user asks about app scripting capabilities.
---

# sdefq — Query macOS AppleScript Dictionaries

Use `${CLAUDE_SKILL_DIR}/sdefq` to discover commands, classes, properties, and enumerations available in scriptable macOS applications. Essential when writing AppleScript or JavaScript for Automation (JXA).

## Usage

### List scriptable apps

```bash
${CLAUDE_SKILL_DIR}/sdefq --list
```

### Show app overview

```bash
${CLAUDE_SKILL_DIR}/sdefq Safari
```

Output:

```
Safari — 1 suite

  Safari suite
    Safari specific classes
    Commands (10): add reading list item, do JavaScript, email contents, ...
    Classes  (5): tab, sourceProvider, contentsProvider, window, document
    Enums    (0): —
```

### Look up a command

```bash
${CLAUDE_SKILL_DIR}/sdefq Safari command "do JavaScript"
```

Output:

```
command: do JavaScript (suite: Safari suite)
  Applies a string of JavaScript code to a document.
  Direct parameter: text (required)
    The JavaScript code to evaluate.
  Parameters:
    in    (optional) — The tab that the JavaScript should be evaluated in.
  Returns: any
```

### Look up a class

```bash
${CLAUDE_SKILL_DIR}/sdefq Safari class tab
```

Output:

```
class: tab (suite: Safari suite)
  A Safari window tab.
  Properties:
    source               text         (r) — The HTML source of the web page ...
    URL                  text         (rw) — The current URL of the tab.
    index                number       (r) — The index of the tab, ordered left to right.
    visible              boolean      (r) — Whether the tab is currently visible.
    name                 text         (r) — The name of the tab.
  Responds to: do JavaScript, email contents, close, search the web
```

### Look up an enumeration

```bash
${CLAUDE_SKILL_DIR}/sdefq Keynote enum "export format"
```

### List all commands/classes/enums

```bash
${CLAUDE_SKILL_DIR}/sdefq Safari command      # all commands
${CLAUDE_SKILL_DIR}/sdefq Safari class        # all classes
${CLAUDE_SKILL_DIR}/sdefq Safari enum         # all enumerations
```

### View a suite

```bash
${CLAUDE_SKILL_DIR}/sdefq Safari "Safari suite"
```

### Search across the dictionary

```bash
${CLAUDE_SKILL_DIR}/sdefq Safari --search JavaScript
```

## Tips

- Names are case-insensitive
- Quote multi-word names: `"do JavaScript"`, not `do JavaScript`
- Check the app overview first to see available suites
- `(r)` = read-only property, `(rw)` = read-write
- `Responds to:` shows which commands work with a class

## Workflow

When helping write AppleScript/JXA for an app:

1. `${CLAUDE_SKILL_DIR}/sdefq AppName` — see what's available
2. `${CLAUDE_SKILL_DIR}/sdefq AppName command "name"` — get command signature
3. `${CLAUDE_SKILL_DIR}/sdefq AppName class "name"` — get properties and elements
4. Use the discovered types and parameters to write correct scripts
