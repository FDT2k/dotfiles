# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Linux desktop environment configuration system centered around **Qtile window manager**. Contains dotfiles, shell scripts, and automation tools for a customizable workspace.

## Setup

```bash
# Install dependencies
bin/install-deps.sh

# Symlink qtile_config package to Qtile config directory
ln -sf $(pwd)/qtile_config ~/.config/qtile/qtile_config

# Create config.py that imports the package
echo "from qtile_config import *" > ~/.config/qtile/config.py

# Initialize desktop environment
./autostart.sh

# Restart Qtile after config changes
qtile cmd-obj -o cmd -f restart

# Verify syntax
python3 -m py_compile qtile_config/__init__.py
```

## Architecture

### Qtile Config Package (`qtile_config/`)

Modular Python package structure:

| Module | Purpose |
|--------|---------|
| `__init__.py` | Entry point - exports Qtile variables, floating_layout, config |
| `themes.py` | Pywal colors integration, `theme` and `theme_neg` classes |
| `commands.py` | Key modifiers (`mod`, `alt`, `ctrl`, `shft`) + script paths |
| `workspaces.py` | Workspaces, rooms, groups, ScratchPad, `workspace_keys` |
| `layouts.py` | Layout definitions (Max, Bsp, TreeTab), widget_defaults |
| `keybindings.py` | All key and mouse bindings |
| `screens.py` | Screen and bar configurations |
| `hooks.py` | Qtile hook subscriptions (screen_change, client_new, startup) |

**Dependency order:**
```
Level 0: themes.py, commands.py (no internal deps)
Level 1: workspaces.py, layouts.py, hooks.py
Level 2: keybindings.py, screens.py
Level 3: __init__.py (imports all)
```

### Workspace/Room System

The Qtile configuration implements a two-level workspace organization:
- **Workspaces** (F1-F6): Top-level context switching
- **Rooms** (a-d): Sub-workspaces within each workspace
- Groups are dynamically shown/hidden based on active workspace
- State persisted across sessions
- **Modular**: `workspace_keys` can be disabled by commenting one line in `keybindings.py`

### Dynamic Menu System

The `bin/` directory uses a `.d` directory pattern for pluggable menus:
- `browser.d/` - Browser selection
- `configure.d/` - Configuration tools
- `power.d/` - Power management (lock, suspend, shutdown)
- `pacman.d/` - Package management operations
- `sound.d/` - Audio output selection
- `worklayout.d/` - Workspace layout presets

`bin/run.sh` reads these directories and presents options via Rofi.

### Color/Theme System

- Pywal generates themes stored in `~/.cache/wal/colors.json`
- `bin/theme/` scripts apply colors to various components:
  - `pick` - Theme selector
  - `reload` - Apply theme to Qtile
  - `colorize-dunst` - Notification styling
  - `colorize-k70` - Keyboard RGB

### Monitor Configuration

Preset layouts in `bin/monitor_layout/`:
- `home-layout.sh`, `vertical_layout.sh`
- `samsung-uwide-*.sh` - Ultrawide configurations

## Key Files

| File | Purpose |
|------|---------|
| `qtile_config/` | Modular Qtile configuration package (see Architecture) |
| `fdt2k.config.py` | Legacy monolithic config (deprecated, kept for reference) |
| `autostart.sh` | Desktop initialization and daemon startup |
| `bin/run.sh` | Rofi-based application/menu launcher |
| `bin/lock` | Screen locking (uses i3lock-multimonitor) |
| `bin/*volume` | Audio control scripts |
| `bin/brightness.sh` | Monitor brightness |

## Dependencies

Core: qtile, python-rofi, rofi, xrandr, ImageMagick, xdotool, pamixer, pactl, pywal, terminator

## Keybinding Conventions

Defined in `qtile_config/commands.py` and `qtile_config/keybindings.py`:
- `mod4` (Super) - Primary modifier
- `mod1` (Alt) - Secondary modifier
- Workspace switching: mod4 + F1-F6 (defined in `workspaces.py`)
- Room switching: mod4 + a/s/d/y/x/c (defined in `workspaces.py`)
- Layout control: mod4 + various keys
- Mouse bindings: mod4 + mouse buttons (defined in `keybindings.py`)
