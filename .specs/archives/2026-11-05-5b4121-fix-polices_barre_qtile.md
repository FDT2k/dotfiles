# Triangles de la barre décollés sur le laptop : police Arial résolue différemment

Status: implemented
Chantier: divers

## Situation initiale

La barre du premier écran (`.config/qtile/qtile_config/screens.py`) encadre ses deux blocs colorés (rooms à gauche, graphes à droite) de triangles `◢` / `◤`. Ce sont quatre `widget.TextBox` en `font="Arial"`, très grands (`fontsize=FONT_SIZE*5.25`) et avec `padding=-1`, pour qu'ils touchent les blocs. La `GroupBox` est en `font='Open Sans'`. Le `widget_defaults` de `layouts.py` est en `font='sans'`.

Aucune de ces polices n'est installée par `.config/qtile/bin/install-arch-deps.sh` : le rendu dépend de ce que fontconfig trouve sur la machine. Constaté par l'humain :

| Machine | `fc-match Arial` |
|---|---|
| poste fixe (daoloth) | `Arimo-Regular.ttf: "Arimo" "Regular"` |
| laptop (abhoth) | `Roboto-Regular.ttf: "Roboto" "Regular"` |

Arimo est la police métriquement compatible avec Arial, du paquet `ttf-croscore`. Roboto ne l'est pas : ses glyphes `◢` / `◤` ont d'autres approches.

## Problème

- **Symptôme** : sur le laptop, de petits espaces séparent les triangles du bloc des rooms et du bloc des graphes. Sur le poste fixe, ils sont collés.
- **Déclencheur** : une machine où `Arial` n'est pas résolu en Arimo (police absente ou autre alias fontconfig).
- **Impact** : la barre n'a pas le même rendu d'une machine à l'autre, et l'effet de bloc continu est cassé sur le laptop.

## Comportement attendu

1. Les quatre triangles utilisent **`font="Arimo"`**, nommé explicitement. On ne dépend plus de l'alias fontconfig de `Arial`. Le rendu est celui du poste fixe.
2. La `GroupBox` garde `font='Open Sans'`, désormais installée partout.
3. `install-arch-deps.sh` a un groupe **`fonts`**, installé par défaut, qui fournit les polices de la barre : `ttf-croscore` (Arimo) et `ttf-opensans` (Open Sans), tous deux dans les dépôts officiels.
4. Le poste fixe ne change pas visuellement : `Arial` y donnait déjà Arimo.

> Invariants : tailles, `padding`, couleurs et textes des triangles inchangés ; même config pour qtile 0.34 et 0.37.

## Comportement actuel (avant fix)

- `screens.py` : 4 × `font="Arial"`.
- `install-arch-deps.sh` : aucun groupe ne fournit Arimo ni Open Sans.

## Cause identifiée

- `.config/qtile/qtile_config/screens.py` (les quatre `TextBox` des triangles) — police demandée par un nom (`Arial`) que fontconfig résout différemment selon les polices installées.
- `.config/qtile/bin/install-arch-deps.sh` — les polices de la barre ne sont pas installées : chaque machine a ses propres substituts.

## Solution

### `screens.py`

`font="Arial"` → `font="Arimo"` sur les quatre `TextBox` `◢` / `◤`. Rien d'autre ne change.

### `install-arch-deps.sh`

- `FONTS_PKGS=(ttf-croscore ttf-opensans)`, commenté : polices de la barre Qtile (Arimo pour les triangles, Open Sans pour la GroupBox).
- Cas `fonts` du `case`, groupe ajouté aux groupes par défaut après `screens`, au message de groupe inconnu et à l'en-tête.

### Documentation

`.config/qtile/CLAUDE.md` : groupe `fonts` dans la ligne d'usage du script.

## Contraintes à respecter

- Dépôts officiels seulement.
- Ne pas toucher à `widget_defaults` (`font='sans'`) ni aux polices de rofi (Hack, groupe `rofi`).
- Ne pas modifier `fontsize` ni `padding` des triangles.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Les cas se jouent par commande et avec la fausse `libqtile` des specs précédentes, puis à l'œil sur le laptop.

| Cas | Attendu |
|-----|---------|
| `python3 -m py_compile .config/qtile/qtile_config/*.py` ; `bash -n install-arch-deps.sh` | aucune erreur |
| Reproduit le bug — avant fix, `grep -c 'font="Arial"' screens.py` | 4 |
| Après fix, `grep -c 'font="Arial"' screens.py` / `grep -c 'font="Arimo"' screens.py` | 0 / 4 |
| Après fix, `screens.py` chargé avec la fausse `libqtile` | les 4 triangles ont `font == "Arimo"`, mêmes `text`, `fontsize`, `padding`, `foreground` qu'avant |
| `install-arch-deps.sh fonts` (faux `sudo`) | pacman reçoit `ttf-croscore ttf-opensans`, aucun appel git |
| `install-arch-deps.sh` sans argument | `ttf-croscore` et `ttf-opensans` présents |
| `install-arch-deps.sh foo` | message listant `fonts`, code 2 |
| Laptop — après `install-arch-deps.sh fonts` et redémarrage de Qtile | `fc-match Arimo` donne Arimo ; triangles collés aux blocs, comme sur le poste fixe |
