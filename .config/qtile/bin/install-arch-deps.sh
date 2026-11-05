#!/bin/bash
# Install the Arch packages for rofi, the theme/wallpaper chain (hellwal) and
# the screen lock (i3lock-multimonitor).
#
#   install-arch-deps.sh                 # every group
#   install-arch-deps.sh rofi lock       # only the named groups: rofi, theme, lock
#
# Official repositories only (pacman), no AUR: packages already installed are
# skipped (--needed). hellwal is not in the official repositories: the script
# only checks that a binary is found where hellwal-apply looks for it.

set -e

DIR="$(cd "$(dirname "$0")" && pwd)"

# rofi menus: the themes use the Hack font and Papirus icons
ROFI_PKGS=(rofi ttf-hack papirus-icon-theme)
# bin/theme/pick, reload, hellwal-apply: pixelated wallpaper (convert),
# failure notification, wallpaper read from colors.json (python)
THEME_PKGS=(imagemagick libnotify python)
# bin/i3lock-multimonitor/lock (i3lock, convert, xrandr), locked on suspend
# by xss-lock (autostart.sh)
LOCK_PKGS=(i3lock xss-lock imagemagick xorg-xrandr)

groups=("$@")
[ ${#groups[@]} -eq 0 ] && groups=(rofi theme lock)

pkgs=()
want_hellwal=no
for g in "${groups[@]}"; do
    case "$g" in
        rofi)  pkgs+=("${ROFI_PKGS[@]}") ;;
        theme) pkgs+=("${THEME_PKGS[@]}"); want_hellwal=yes ;;
        lock)  pkgs+=("${LOCK_PKGS[@]}") ;;
        *)     echo "unknown group: $g (rofi, theme, lock)" >&2; exit 2 ;;
    esac
done

# Deduplicate, keep order
mapfile -t pkgs < <(printf '%s\n' "${pkgs[@]}" | awk '!seen[$0]++')

echo "==> pacman: ${pkgs[*]}"
sudo pacman -S --needed "${pkgs[@]}"

if [ "$want_hellwal" = yes ]; then
    # Same lookup as bin/theme/hellwal-apply
    found=""
    for candidate in "$(command -v hellwal || true)" "$DIR/hellwal" "$HOME/bin/hellwal" "$HOME/.local/bin/hellwal"; do
        if [ -n "$candidate" ] && [ -x "$candidate" ]; then
            found="$candidate"
            break
        fi
    done

    if [ -n "$found" ]; then
        echo "==> hellwal present: $found"
    else
        echo "==> hellwal not found (not in the official repositories):" >&2
        echo "    drop the binary in $DIR/hellwal" >&2
        exit 1
    fi
fi

echo "==> done"
