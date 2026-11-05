# Bizarreries de couleurs dans la barre Qtile : bloc gris fixe, graphes, bordures flottantes

Status: implemented
Chantier: divers

## Situation initiale

La barre du premier écran (`.config/qtile/qtile_config/screens.py`) a deux **blocs colorés**, chacun encadré de flèches `◢` / `◤` :
- **à gauche**, les rooms : `GroupBox` sur `theme_neg.bg` (`color2`), texte `color0`, rooms vides calculées par `readable_dim` (spec `75eeed`, [archive](./2026-11-05-75eeed-fix-groupbox_inactif_illisible.md)) ;
- **à droite**, les graphes `NetGraph`, `CPUGraph`, `MemoryGraph` : fond et flèches en **gris fixe `#CACACA`**, qui ne suit pas le thème. `CPUGraph` et `MemoryGraph` tracent en `theme.bg_active` (`color1`). `NetGraph` n'a ni `graph_color` ni `border_color` : il garde les couleurs par défaut de Qtile.

Les couleurs viennent de `.config/qtile/qtile_config/themes.py`. hellwal tourne en `--comfort-mode`, qui garantit le contraste de chaque couleur contre `color0` : au moins 5.2:1 pour `color1`–`6`, 7.2:1 pour `color7`/`15`.

Dans `.config/qtile/qtile_config/__init__.py`, le layout flottant est déclaré avec `border_normal=theme.fg` (`color7`, clair) et `border_focus=theme.bg` (`color0`, la couleur du fond). Les layouts tilés de `.config/qtile/qtile_config/layouts.py` font l'inverse : `border_focus=theme.bg_active` (`color1`), `border_normal=theme.bg` (`color0`).

## Problème

- **Symptôme** :
  - le bloc de droite reste gris clair quel que soit le thème, et les graphes `color1` y sont plus ou moins lisibles selon l'image ;
  - le `NetGraph` n'a pas les couleurs des deux autres graphes ;
  - une fenêtre flottante qui a le focus a une bordure presque invisible, tandis que les autres flottantes ont une bordure claire.
- **Déclencheur** : tout thème ; toute fenêtre flottante (dialogues, copyq, bitwarden, blueman…).
- **Impact** : la barre n'est pas cohérente avec le thème, et on ne voit pas quelle fenêtre flottante a le focus.

## Comportement attendu

1. **Bloc de droite comme celui des rooms** : les deux flèches et le fond des trois graphes passent de `#CACACA` à `theme_neg.bg` (`color2`). La barre devient symétrique.
2. **Graphes lisibles sur ce bloc** : `graph_color` et `border_color` des trois graphes (`NetGraph` compris) valent `theme_neg.fg` (`color0`). Son contraste contre `color2` est garanti à 5.2:1 au moins par le mode confort.
3. **Bordures des fenêtres flottantes alignées sur les layouts tilés** : `border_focus=theme.bg_active` (`color1`), `border_normal=theme.bg` (`color0`). `border_width=4` est inchangé.
4. Plus aucune couleur en dur dans `screens.py`.

> Invariants : même config pour qtile 0.34 et 0.37 ; aucune couleur de la GroupBox ne change ; les règles flottantes (`float_rules`) ne changent pas.

## Comportement actuel (avant fix)

- `screens.py` contient 5 occurrences de `"#CACACA"` : 2 flèches et 3 fonds de graphe.
- `NetGraph` sans `graph_color` ni `border_color`.
- `__init__.py` : `border_normal=theme.fg, border_focus=theme.bg`.

## Cause identifiée

- `.config/qtile/qtile_config/screens.py` — bloc de droite codé en gris fixe (lignes des `TextBox` `◢` / `◤` et des trois graphes) ; `NetGraph` jamais coloré.
- `.config/qtile/qtile_config/__init__.py` (ligne 45) — `border_normal` et `border_focus` inversés par rapport aux layouts tilés.

## Solution

### `screens.py`

- Les deux `TextBox` du bloc de droite : `foreground="#CACACA"` → `foreground=theme_neg.bg`.
- `NetGraph`, `CPUGraph`, `MemoryGraph` : `background="#CACACA"` → `background=theme_neg.bg`, et `graph_color=theme_neg.fg`, `border_color=theme_neg.fg`, ajoutés au `NetGraph` et remplaçant `theme.bg_active` sur les deux autres.
- Les autres arguments (`type`, `bandwidth_type`, `border_width`, `line_width`) ne changent pas.

### `__init__.py`

`border_normal=theme.fg, border_focus=theme.bg` → `border_normal=theme.bg, border_focus=theme.bg_active`.

## Contraintes à respecter

- Ne pas toucher à la GroupBox ni à `themes.py`.
- Hors périmètre : la bordure de l'écran courant de la GroupBox (`this_current_screen_border`), le `CurrentLayout`, le `WindowName`, la `Clock`.
- Pas de nouveau widget ni de nouvelle couleur dans `themes.py`.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Les cas se jouent avec la fausse `libqtile` minimale des specs précédentes, qui enregistre les arguments des widgets et de `layout.Floating`, puis à l'œil sur le laptop.

| Cas | Attendu |
|-----|---------|
| `python3 -m py_compile .config/qtile/qtile_config/*.py` | aucune erreur |
| Reproduit le bug — avant fix, `grep -c '#CACACA' screens.py` | 5 |
| Après fix, `grep -c '#CACACA' screens.py` | 0 |
| Après fix, flèches du bloc de droite | `foreground == theme_neg.bg` |
| Après fix, les 3 graphes | `background == theme_neg.bg`, `graph_color == border_color == theme_neg.fg` |
| Après fix, palette de secours | `contrast(theme_neg.fg, theme_neg.bg) ≥ 4.5` (lisibilité des graphes) |
| Après fix, `layout.Floating` | `border_focus == theme.bg_active`, `border_normal == theme.bg`, `border_width == 4` |
| Après fix, `GroupBox` | arguments identiques à avant |
| Laptop — barre | bloc de droite de la couleur du bloc des rooms, graphes lisibles, sur plusieurs thèmes |
| Laptop — deux fenêtres flottantes (ex. copyq et un dialogue) | celle qui a le focus a la bordure colorée, l'autre la bordure sombre |
