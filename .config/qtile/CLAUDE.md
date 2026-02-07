# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Linux desktop environment configuration system centered around **Qtile window manager**. Contains dotfiles, shell scripts, and automation tools for a customizable workspace.

## Setup

```bash
# Install dependencies
bin/install-deps.sh

# Copy/symlink config to Qtile config directory
cp fdt2k.config.py ~/.config/qtile/config.py

# Initialize desktop environment
./autostart.sh

# Restart Qtile after config changes
qtile cmd-obj -o cmd -f restart
```

## Architecture

### Workspace/Room System

The Qtile configuration implements a two-level workspace organization:
- **Workspaces** (F1-F6): Top-level context switching
- **Rooms** (a-d): Sub-workspaces within each workspace
- Groups are dynamically shown/hidden based on active workspace
- State persisted across sessions

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
| `fdt2k.config.py` | Main Qtile config (keybindings, layouts, widgets, hooks) |
| `autostart.sh` | Desktop initialization and daemon startup |
| `bin/run.sh` | Rofi-based application/menu launcher |
| `bin/lock` | Screen locking (uses i3lock-multimonitor) |
| `bin/*volume` | Audio control scripts |
| `bin/brightness.sh` | Monitor brightness |

## Dependencies

Core: qtile, python-rofi, rofi, xrandr, ImageMagick, xdotool, pamixer, pactl, pywal, terminator

## Keybinding Conventions

Defined in `fdt2k.config.py`:
- `mod4` (Super) - Primary modifier
- `mod1` (Alt) - Secondary modifier
- Workspace switching: mod4 + F1-F6
- Room switching: mod4 + a/s/d/f
- Layout control: mod4 + various keys
