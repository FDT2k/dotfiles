#!/bin/bash

# Forest tourne sur daoloth, dans la session xpra :101 ; il s'affiche sur la
# machine qui s'y attache (abhoth ou daoloth). Jamais deux Forest sur daoloth :
# il se lance toujours dans la session xpra, jamais sur l'écran de daoloth.
# Paquets : xpra partout, xorg-server-xvfb en plus sur daoloth.
#
# Ne pas utiliser --start-child/--exit-with-children (l'AppImage rend la main,
# xpra arrête la session) ni --start seul (session vide) : Forest se lance à
# part, sur l'affichage de la session. --ssh=ssh garde ~/.ssh/config.

FOREST_HOST=daoloth
FOREST_SSH=fabien@daoloth.lan
FOREST_DISPLAY=101
FOREST_BIN=/home/fabien/bin/forest

# Sur daoloth, la session est locale ; ailleurs, on passe par SSH.
_forest_local() { [ "$(uname -n)" = "$FOREST_HOST" ]; }

_forest_xpra() {
  local cmd=$1; shift
  if _forest_local; then
    xpra "$cmd" ":$FOREST_DISPLAY" "$@"
  else
    xpra "$cmd" "ssh://$FOREST_SSH/$FOREST_DISPLAY" --ssh=ssh "$@"
  fi
}

# Crée la session et y lance Forest : une fois, après un redémarrage de daoloth.
forest-up() {
  _forest_xpra start --attach=no || return
  local run="DISPLAY=:$FOREST_DISPLAY setsid -f $FOREST_BIN >/tmp/forest-xpra.log 2>&1"
  if _forest_local; then
    sh -c "$run"
  else
    ssh "$FOREST_SSH" "$run"
  fi
}

# Affiche Forest sur la machine courante, sans bloquer le shell.
forest-on() {
  if _forest_local; then
    setsid -f xpra attach ":$FOREST_DISPLAY" >/dev/null 2>&1
  else
    setsid -f xpra attach "ssh://$FOREST_SSH/$FOREST_DISPLAY" --ssh=ssh >/dev/null 2>&1
  fi
}

# Détache : Forest continue de tourner sur daoloth.
forest-off() { _forest_xpra detach; }

# Arrête la session et Forest.
forest-stop() { _forest_xpra stop; }
