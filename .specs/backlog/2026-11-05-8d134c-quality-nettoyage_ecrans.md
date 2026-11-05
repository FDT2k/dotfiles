# Nettoyage de ce qui touche aux écrans : presets morts, anciennes machines, luminosité cassée

Status: draft
Chantier: divers

## Situation actuelle

Inventaire de tout ce qui touche aux écrans dans `.config/qtile/`, avec l'état constaté avec l'humain :

**Code mort (jamais appelé)**
- `bin/monitor_layout/` : 4 scripts xrandr (`home-layout.sh`, `vertical_layout.sh`, `samsung-uwide-no-edp.sh`, `samsung-uwide-with-edp.sh`) pour un ancien laptop (`eDP-1`, `HDMI-1`). Ce sont des doublons de `screenlayout.d/home`, `vertical`, `samsung`, `samsung-dual`.
- `qtile_config/keybindings.py` : 4 fonctions `set_vertical_monitor_layout`, `set_horizontal_monitor_layout`, `set_samsung_monitor_layout`, `set_samsung_monitor_dual_layout` qui les lancent. Aucun `Key` ne les appelle.
- `qtile_config/commands.py` : leurs 4 entrées `home_screen_layout`, `work_screen_layout`, `samsung_screen_layout`, `samsung_screen_dual_layout`, utilisées par ces fonctions seulement.

**Fonction abandonnée par l'humain**
- `toggle_screen_focus` (`Key([mod], "q", …)`) fait tourner le focus sur 3 écrans (middle/right/left), avec une notification. Elle appelle `move_cursor`, qui lit `xrandr` et déplace la souris avec `xdotool`. `move_cursor` n'est utilisée que là, tout comme la variable globale `curr_screen` et `import subprocess`.

**Luminosité cassée sur le fixe**
- `Key([mod, alt], "1"|"2"|"3", …)` lancent `command.left/middle/right_screen_brightness`, c'est-à-dire `bin/brightness.sh HDMI-A-1-0 | HDMI-A-1 | DVI-I-1`. Ce script demande une valeur dans rofi puis fait `xrandr --brightness` sur ces sorties, qui sont celles d'une ancienne configuration du fixe. Le fixe actuel a `DisplayPort-4/5/6/7`, donc ces raccourcis ne font plus rien.

**Menu « Monitor Layout »** (`bin/run.sh screenlayout.d`, `mod+alt+l`) : 14 entrées.

| Entrée | Sorties | Sort |
|---|---|---|
| `daoloth.sh` | `DisplayPort-4/5/6/7` | **gardée** (fixe actuel) |
| `sddm` → `daoloth.sh` (lien) | — | **gardé** : lancé par SDDM avant le login (spec `861406`) |
| `arandr` | — | **gardé** |
| `_daoloth.sh`, `__daoloth.sh`, `sddm.sh` | `HDMI-A-1`, `DVI-I-1`, `HDMI-0` | anciennes versions du fixe, **supprimées** |
| `home`, `vertical`, `samsung`, `samsung-dual` | `eDP-1`, `HDMI-1` | ancien laptop qui n'existe plus, **supprimées** |
| `alienware`, `alien-thin`, `alien-sam-pip-right` | `eDP1`, `HDMI-1-3` | ancienne machine qui n'existe plus, **supprimées** |

## Motivation

- **Contexte** : les dotfiles portent des réglages d'écrans de machines disparues et des raccourcis morts ou cassés. On s'y perd au moment de préparer une configuration par machine (fixe daoloth, laptop abhoth).
- **Objectif** : ne garder que ce qui sert sur les machines actuelles.
- **Bénéfice** : un menu « Monitor Layout » à trois entrées utiles, moins de code mort, et une base propre pour la logique par machine.

## Changements prévus

### Fichiers supprimés (`git rm`)

- `.config/qtile/bin/monitor_layout/` en entier (4 scripts).
- `.config/qtile/bin/brightness.sh`.
- Dans `.config/qtile/bin/screenlayout.d/` : `_daoloth.sh`, `__daoloth.sh`, `sddm.sh`, `home`, `vertical`, `samsung`, `samsung-dual`, `alienware`, `alien-thin`, `alien-sam-pip-right`.

Restent dans `screenlayout.d/` : `daoloth.sh`, `sddm` (lien), `arandr`.

### `qtile_config/keybindings.py`

- Supprimer les 4 fonctions `set_*_monitor_layout`, `toggle_screen_focus`, `move_cursor`, la variable `curr_screen` et son commentaire, et `import subprocess`, devenu inutile.
- Supprimer les `Key` `[mod] "q"` (`toggle_screen_focus`) et `[mod, alt] "1"`, `"2"`, `"3"` (luminosité).
- Rien d'autre ne change : `toggle_center`, `run_prompt`, `pick_theme`, `mod+alt+l` (menu « Monitor Layout ») et tous les autres raccourcis restent.

### `qtile_config/commands.py`

Supprimer les 7 entrées `home_screen_layout`, `work_screen_layout`, `samsung_screen_layout`, `samsung_screen_dual_layout`, `middle_screen_brightness`, `right_screen_brightness`, `left_screen_brightness`. `screen_layout` (le menu) reste.

### Documentation et commentaires

- `.config/qtile/CLAUDE.md` :
  - la section « Monitor Configuration » décrit le menu `screenlayout.d/` (`daoloth.sh`, `sddm` lancé par SDDM, `arandr`) à la place de `bin/monitor_layout/` ;
  - la ligne `bin/brightness.sh` du tableau « Key Files » est retirée ;
  - `xdotool` est retiré de la liste « Core » des dépendances.
- `.config/qtile/bin/install-arch-deps.sh` : le commentaire du groupe `screens` ne mentionne plus `bin/monitor_layout/`.

## Fichiers concernés

| Fichier | Modification |
|---------|-------------|
| `.config/qtile/bin/monitor_layout/*` | supprimés |
| `.config/qtile/bin/brightness.sh` | supprimé |
| `.config/qtile/bin/screenlayout.d/` (10 fichiers listés) | supprimés |
| `.config/qtile/qtile_config/keybindings.py` | fonctions, variable, import et 4 `Key` retirés |
| `.config/qtile/qtile_config/commands.py` | 7 entrées retirées |
| `.config/qtile/CLAUDE.md` | « Monitor Configuration », « Key Files », dépendances |
| `.config/qtile/bin/install-arch-deps.sh` | commentaire du groupe `screens` |

## Contraintes à respecter

- Ne pas toucher à `daoloth.sh`, au lien `sddm` ni à `arandr`.
- Ne pas modifier `bin/run.sh` ni le raccourci `mod+alt+l`.
- Ne pas libérer d'autre raccourci que `mod+q` et `mod+alt+1/2/3`.
- Pas de logique par machine dans cette spec (à venir).
- `xorg-xrandr` reste dans le groupe `screens` : `daoloth.sh` l'utilise.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Les cas se jouent par commande et en Python, avec une fausse `libqtile` qui enregistre les `Key`, puis à l'usage sur les deux machines.

| Cas | Attendu |
|-----|---------|
| `python3 -m py_compile .config/qtile/qtile_config/*.py` | aucune erreur |
| `ls .config/qtile/bin/screenlayout.d/` | exactement `arandr`, `daoloth.sh`, `sddm` (lien vers `daoloth.sh`) |
| `ls .config/qtile/bin/monitor_layout .config/qtile/bin/brightness.sh` | absents |
| `grep -rn "monitor_layout\|brightness\|toggle_screen_focus\|move_cursor\|curr_screen\|_screen_layout\b" .config/qtile/qtile_config` | aucun résultat, hormis `screen_layout` (menu) |
| `keybindings.py` chargé avec la fausse `libqtile` | plus de `Key` `[mod] q` ni `[mod, alt] 1/2/3` ; même nombre de `Key` qu'avant moins 4 ; `mod+alt+l` et `mod+shift+f` toujours présents |
| `grep -rn "screenlayout.d/\(home\|vertical\|samsung\|alien\|_daoloth\|sddm.sh\)" .` (hors `.specs/`) | aucun résultat |
| Fixe — `mod+alt+l` | menu à trois entrées ; `daoloth.sh` règle les écrans |
| Fixe — démarrage | SDDM règle toujours les écrans (lien `sddm` intact) |
