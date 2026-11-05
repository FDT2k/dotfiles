#!/bin/bash
# Install the Arch packages for rofi, the theme/wallpaper chain (hellwal),
# the screen lock (i3lock-multimonitor), notifications (dunst), the
# terminal (terminator), the screen layouts (arandr, xrandr) and the Qtile bar
# fonts; the group sddm (never installed by default) also configures SDDM.
#
#   install-arch-deps.sh                 # every group
#   install-arch-deps.sh rofi lock       # only the named groups: rofi, theme, lock, dunst, terminator, screens, fonts
#   install-arch-deps.sh sddm            # SDDM, its config and the fdt2k-dark theme (not in the default groups)
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
# Login screen: SDDM, configured by setup_sddm (screen layout before the
# login, fdt2k-dark theme). Touches the system: not a default group.
# The theme runs on the Qt 6 greeter (QtVersion=6): Qt5Compat.GraphicalEffects
# for its shadows, svg for its icons, the virtual keyboard component.
SDDM_PKGS=(sddm qt6-5compat qt6-svg qt6-virtualkeyboard)

# SDDM paths, overridable for tests
SDDM_CONF_DIR="${SDDM_CONF_DIR:-/etc/sddm.conf.d}"
SDDM_THEMES_DIR="${SDDM_THEMES_DIR:-/usr/share/sddm/themes}"
SDDM_THEME=fdt2k-dark

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

# Point SDDM at the dotfiles: /etc/sddm.conf.d/10-dotfiles.conf (theme and
# screen layout run before the login) and a link from the SDDM themes dir to
# the theme versioned in ~/.local/share/sddm/themes. Never touches Xsetup,
# never changes permissions: it only says what to do.
setup_sddm() {
    local layout="$HOME/.config/qtile/bin/screenlayout.d/sddm"
    local theme_src="$HOME/.local/share/sddm/themes/$SDDM_THEME"
    local theme_dst="$SDDM_THEMES_DIR/$SDDM_THEME"
    local wallpaper="$HOME/.cache/wal/current-theme.jpg"
    local conf="$SDDM_CONF_DIR/10-dotfiles.conf"

    echo "==> sddm: writing $conf"
    sudo mkdir -p "$SDDM_CONF_DIR"
    printf '%s\n' \
        "# Written by ~/.config/qtile/bin/install-arch-deps.sh (group sddm)" \
        "[Theme]" \
        "Current=$SDDM_THEME" \
        "" \
        "[X11]" \
        "DisplayCommand=$layout" | sudo tee "$conf" >/dev/null
    sudo chmod 644 "$conf"
    [ -x "$layout" ] || echo "==> warning: $layout missing or not executable: SDDM will run it before the login screen" >&2

    if [ ! -d "$theme_src" ]; then
        echo "==> warning: $theme_src missing: theme $SDDM_THEME not linked" >&2
    elif [ -L "$theme_dst" ] && [ "$(readlink "$theme_dst")" = "$theme_src" ]; then
        echo "==> sddm: theme already linked: $theme_dst"
    else
        if [ -e "$theme_dst" ] || [ -L "$theme_dst" ]; then
            local backup
            backup="$theme_dst.bak-$(date +%Y%m%d-%H%M%S)"
            echo "==> sddm: keeping the previous theme as $backup"
            sudo mv "$theme_dst" "$backup"
        fi
        sudo ln -s "$theme_src" "$theme_dst"
        echo "==> sddm: theme linked: $theme_dst → $theme_src"
    fi

    # The greeter runs as user sddm: it must read the theme and the wallpaper
    if ! id sddm >/dev/null 2>&1; then
        echo "==> warning: no sddm user: cannot check that the greeter reads the theme" >&2
    else
        local unreadable=() f d
        [ -d "$theme_src" ] && ! sudo -u sddm test -r "$theme_dst/Main.qml" && unreadable+=("$theme_src/Main.qml")
        [ -f "$wallpaper" ] && ! sudo -u sddm test -r "$wallpaper" && unreadable+=("$wallpaper")
        if [ ${#unreadable[@]} -gt 0 ]; then
            local blocking=()
            for f in "${unreadable[@]}"; do
                d="$(dirname "$f")"
                while [ "$d" != "/" ]; do
                    [ $(( $(stat -c %a "$d") % 2 )) -eq 1 ] || blocking+=("$d")
                    d="$(dirname "$d")"
                done
            done
            mapfile -t blocking < <(printf '%s\n' "${blocking[@]}" | awk 'NF && !seen[$0]++' | sort)
            echo "==> warning: the sddm user cannot read ${unreadable[*]}" >&2
            if [ ${#blocking[@]} -gt 0 ]; then
                echo "    not traversable by others: ${blocking[*]}" >&2
                echo "    to fix it: chmod o+x ${blocking[*]}" >&2
            fi
            echo "    otherwise SDDM falls back to its default theme" >&2
        fi
    fi

    echo "==> sddm: /usr/share/sddm/scripts/Xsetup is not used anymore: a 'source …screenlayout.d/sddm' line added by hand there can be removed"
    [ -f "$SDDM_CONF_DIR/sddm.conf" ] && echo "==> sddm: $SDDM_CONF_DIR/sddm.conf is redundant with the [Theme] section of 10-dotfiles.conf"
    [ "$(systemctl is-enabled sddm 2>/dev/null)" = enabled ] || echo "==> sddm: enable it with: sudo systemctl enable sddm"
}

groups=("$@")
[ ${#groups[@]} -eq 0 ] && groups=(rofi theme lock dunst terminator screens fonts)

pkgs=()
want_hellwal=no
want_sddm=no
for g in "${groups[@]}"; do
    case "$g" in
        rofi)  pkgs+=("${ROFI_PKGS[@]}") ;;
        theme) pkgs+=("${THEME_PKGS[@]}"); want_hellwal=yes ;;
        lock)  pkgs+=("${LOCK_PKGS[@]}") ;;
        dunst) pkgs+=("${DUNST_PKGS[@]}") ;;
        terminator) pkgs+=("${TERMINATOR_PKGS[@]}") ;;
        screens) pkgs+=("${SCREENS_PKGS[@]}") ;;
        fonts) pkgs+=("${FONTS_PKGS[@]}") ;;
        sddm)  pkgs+=("${SDDM_PKGS[@]}"); want_sddm=yes ;;
        *)     echo "unknown group: $g (rofi, theme, lock, dunst, terminator, screens, fonts, sddm)" >&2; exit 2 ;;
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

if [ "$want_sddm" = yes ]; then
    setup_sddm
fi

echo "==> done"
