#!/bin/bash
# Install the Arch packages for rofi, the theme/wallpaper chain (hellwal),
# the screen lock (i3lock-multimonitor), notifications (dunst), the
# terminal (terminator), the screen layouts (arandr, xrandr) and the Qtile bar
# fonts.
#
#   install-arch-deps.sh                 # every group
#   install-arch-deps.sh rofi lock       # only the named groups: rofi, theme, lock, dunst, terminator, screens, fonts
#
# Official repositories only (pacman), no AUR: packages already installed are
# skipped (--needed). Tools that are not packaged are built from git (see
# git_install): cloned in ~/.local/src/<name>, updated, built with make and
# copied to ~/bin/<name> on every run.

set -e

DIR="$(cd "$(dirname "$0")" && pwd)"

# rofi menus: the themes use the Hack font and Papirus icons
ROFI_PKGS=(rofi ttf-hack papirus-icon-theme)
# bin/theme/pick, reload, hellwal-apply: pixelated wallpaper (convert),
# failure notification, wallpaper read from colors.json (python);
# git, make, gcc to build hellwal
THEME_PKGS=(imagemagick libnotify python git make gcc)
# bin/i3lock-multimonitor/lock (i3lock, convert, xrandr), locked on suspend
# by xss-lock (autostart.sh)
LOCK_PKGS=(i3lock xss-lock imagemagick xorg-xrandr)
# Notifications: dunst, recolored by bin/theme/colorize-dunst; notify-send
DUNST_PKGS=(dunst libnotify)
# Terminal: Qtile's terminal, ScratchPad dropdown and bin/floatterm
# (profiles and layouts in ~/.config/terminator/config)
TERMINATOR_PKGS=(terminator)
# Screen layouts: arandr entry of the screenlayout.d menu; xrandr for the
# other entries
SCREENS_PKGS=(arandr xorg-xrandr)
# Qtile bar fonts: Arimo (ttf-croscore) for the ◢ ◤ arrows, Open Sans for the
# GroupBox
FONTS_PKGS=(ttf-croscore ttf-opensans)

# Git recipes: name, repository, binary built by make (relative to the repo)
HELLWAL_GIT=(hellwal https://github.com/FDT2k/hellwal.git hellwal)

# Clone (or update) a repository in ~/.local/src/<name>, build it with make
# and copy the binary to ~/bin/<name>. Any failure stops the script; the
# binary already in ~/bin is only replaced once the build succeeded.
git_install() {
    local name="$1" url="$2" binary="$3"
    local src="$HOME/.local/src/$name"

    fail() {
        echo "==> $name: $1" >&2
        exit 1
    }

    echo "==> git: $name ($url) → ~/bin/$name"
    if [ -e "$src" ]; then
        [ -d "$src/.git" ] || fail "$src exists and is not a git repository"
        git -C "$src" pull --ff-only || fail "pull failed in $src"
    else
        mkdir -p "$HOME/.local/src"
        git clone "$url" "$src" || fail "clone failed: $url"
    fi
    make -C "$src" || fail "make failed in $src"
    [ -f "$src/$binary" ] || fail "binary not found: $src/$binary"

    mkdir -p "$HOME/bin"
    install -m 755 "$src/$binary" "$HOME/bin/$name"
    echo "==> $name installed: ~/bin/$name"
}

# Warn when another hellwal would be found before ~/bin/hellwal by
# bin/theme/hellwal-apply (PATH first, then ~/.config/qtile/bin)
warn_hellwal_shadowed() {
    local fresh shadow
    fresh="$(realpath "$HOME/bin/hellwal")"
    for shadow in "$(command -v hellwal || true)" "$DIR/hellwal"; do
        [ -n "$shadow" ] && [ -x "$shadow" ] || continue
        [ "$(realpath "$shadow")" = "$fresh" ] && continue
        echo "==> warning: $shadow shadows ~/bin/hellwal for hellwal-apply — remove it to use the fresh build" >&2
    done
}

groups=("$@")
[ ${#groups[@]} -eq 0 ] && groups=(rofi theme lock dunst terminator screens fonts)

pkgs=()
want_hellwal=no
for g in "${groups[@]}"; do
    case "$g" in
        rofi)  pkgs+=("${ROFI_PKGS[@]}") ;;
        theme) pkgs+=("${THEME_PKGS[@]}"); want_hellwal=yes ;;
        lock)  pkgs+=("${LOCK_PKGS[@]}") ;;
        dunst) pkgs+=("${DUNST_PKGS[@]}") ;;
        terminator) pkgs+=("${TERMINATOR_PKGS[@]}") ;;
        screens) pkgs+=("${SCREENS_PKGS[@]}") ;;
        fonts) pkgs+=("${FONTS_PKGS[@]}") ;;
        *)     echo "unknown group: $g (rofi, theme, lock, dunst, terminator, screens, fonts)" >&2; exit 2 ;;
    esac
done

# Deduplicate, keep order
mapfile -t pkgs < <(printf '%s\n' "${pkgs[@]}" | awk '!seen[$0]++')

echo "==> pacman: ${pkgs[*]}"
sudo pacman -S --needed "${pkgs[@]}"

if [ "$want_hellwal" = yes ]; then
    git_install "${HELLWAL_GIT[@]}"
    warn_hellwal_shadowed
fi

echo "==> done"
