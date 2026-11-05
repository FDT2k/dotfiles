# Texte des groupes inactifs illisible dans la GroupBox de la barre Qtile

Status: draft
Chantier: divers

## Situation initiale

La barre du premier écran (`.config/qtile/qtile_config/screens.py`) affiche les groupes (rooms) du workspace courant dans un `widget.GroupBox`. Celui-ci est posé sur un **bloc coloré** encadré de deux flèches `◢` / `◤`, toutes de la couleur `theme_neg.bg` :

| Argument du `GroupBox` | Valeur | Couleur |
|---|---|---|
| `background` | `theme_neg.bg` | `color2` |
| `foreground`, `active` (groupes avec fenêtres) | `theme_neg.fg` | `color0` |
| `inactive` (groupes vides) | `theme_neg.contrasted` | `color7` |
| `this_current_screen_border` | `theme.bg` | `color0` |

Les couleurs viennent de `.config/qtile/qtile_config/themes.py` (`theme`, `theme_neg`), lues dans `~/.cache/wal/colors.json`. Ce fichier est généré par hellwal avec `--comfort-mode` (`bin/theme/hellwal-apply`). Ce mode garantit le contraste de chaque couleur **contre `color0`** : 5.2:1 pour `color1`–`6`, 7.2:1 pour `color7`/`15`.

`theme_neg.contrasted` n'est utilisé que pour `inactive`.

## Problème

- **Symptôme** : dans la GroupBox, le nom des groupes vides est souvent illisible. C'était déjà le cas avec pywal sur le poste fixe.
- **Déclencheur** : `color7` (texte clair) posé sur `color2` (couleur d'accent, claire dès que le fond `color0` est sombre). Le contraste entre les deux n'est garanti par rien, ni par pywal ni par le mode confort, qui ne mesure que contre `color0`.
- **Impact** : les rooms vides du workspace courant ne se lisent pas, selon l'image du thème.

## Comportement attendu

1. Le bloc coloré, les flèches, le fond `color2` et le texte actif `color0` ne changent pas.
2. Le texte des groupes inactifs est une couleur **calculée** dans `themes.py` :
   - le texte actif (`theme_neg.fg`) atténué vers le fond du bloc (`theme_neg.bg`) ;
   - le plus atténué possible tant que son contraste contre le fond reste **≥ 3:1** (seuil WCAG pour le texte large et les éléments d'interface).

   Il reste donc visiblement plus discret que les groupes actifs, et toujours lisible.
3. Si le texte actif lui-même a moins de 3:1 contre le fond du bloc, `inactive` vaut le texte actif : rien de plus lisible n'est atteignable sans changer le design.
4. Le calcul vaut pour toutes les palettes, y compris `DEFAULT_COLORS` (palette de secours de `themes.py`).

> Invariants : même config pour qtile 0.34 et 0.37 ; aucun autre widget ni couleur ne change ; `--comfort-mode` reste actif.

## Comportement actuel (avant fix)

- Groupe vide → texte `color7` sur `color2`, contraste souvent proche de 1:1 à 2:1.
- Exemple, palette de secours de `themes.py` : `color7` `#c5c8c6` sur `color2` `#b5bd68` → contraste ≈ 1.2:1.

## Cause identifiée

- `.config/qtile/qtile_config/screens.py` (ligne 38) — `inactive=theme_neg.contrasted`, soit `color7`, choisi sans tenir compte du fond `color2` du bloc.
- `.config/qtile/qtile_config/themes.py` (classe `theme_neg`) — aucune couleur pensée pour être lue sur `theme_neg.bg`, hormis `theme_neg.fg`.

## Solution

### `themes.py`

Ajouter, au même niveau que `load_colors()` :
- `luminance(hex)` — luminance relative WCAG d'une couleur `#rrggbb` ;
- `contrast(a, b)` — rapport de contraste WCAG, `(L1 + 0.05) / (L2 + 0.05)` avec `L1 ≥ L2` ;
- `mix(a, b, t)` — mélange linéaire composante par composante, `t` = part de `b` (0 → `a`, 1 → `b`), résultat `#rrggbb` ;
- `readable_dim(fg, bg, min_ratio=3.0)` — essaie `mix(fg, bg, t)` pour `t` de 0.95 à 0 par pas de 0.05, et renvoie le premier dont `contrast(·, bg) ≥ min_ratio`. Sinon il renvoie `fg`.

Dans `theme_neg`, ajouter `inactive = readable_dim(fg, bg)`. Le calcul se fait à la définition de la classe, après `bg` et `fg`.

### `screens.py`

`inactive=theme_neg.contrasted` → `inactive=theme_neg.inactive`. Rien d'autre ne change.

## Contraintes à respecter

- Ne changer ni `theme_neg.bg`, ni `theme_neg.fg`, ni les flèches, ni les autres arguments du `GroupBox`.
- Garder `theme_neg.contrasted` (attribut existant), même s'il n'est plus utilisé par la GroupBox.
- Pas de dépendance Python nouvelle : calcul en Python pur.
- Hors périmètre : le gris `#CACACA` des graphes, les bordures des fenêtres flottantes, `this_current_screen_border`.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Les cas se jouent en Python sur `themes.py`, avec la fausse `libqtile` minimale déjà utilisée pour les specs précédentes, puis à l'œil sur le laptop.

| Cas | Attendu |
|-----|---------|
| `python3 -m py_compile .config/qtile/qtile_config/*.py` | aucune erreur |
| `contrast('#000000', '#ffffff')` | 21.0 (± 0.01) ; `contrast(x, x)` = 1.0 |
| `mix('#000000', '#ffffff', 0)` / `1` / `0.5` | `#000000` / `#ffffff` / `#808080` ou `#7f7f7f` |
| Reproduit le bug — palette de secours, `contrast(color7, color2)` | < 3 |
| Après fix, palette de secours | `contrast(theme_neg.inactive, theme_neg.bg) ≥ 3` ; `theme_neg.inactive != theme_neg.fg` ; contraste de `inactive` < contraste de `fg` (plus discret) |
| Après fix, palette où `contrast(fg, bg) < 3` (ex. `color0` `#777777`, `color2` `#888888`) | `theme_neg.inactive == theme_neg.fg` |
| Après fix, 50 palettes aléatoires où `contrast(color0, color2) ≥ 3` | `contrast(inactive, color2) ≥ 3` à chaque fois |
| `screens.py` chargé avec la fausse `libqtile` | `GroupBox` reçoit `inactive == theme_neg.inactive` ; `active`, `background` inchangés |
| Laptop — barre, workspace avec des rooms vides | noms des rooms vides lisibles, plus discrets que les rooms occupées, sur plusieurs thèmes |
