# Rendre la config Qtile compatible avec qtile 0.37 (appels `cmd_*` retirés, hook `screen_change` cassé)

Status: draft
Chantier: divers

## Situation initiale

La même config Qtile (`.config/qtile/qtile_config/`) tourne sur deux machines :

- le poste fixe, figé en **qtile 0.34.1** ;
- le nouveau laptop, en **qtile 0.37.1**.

Elle a été écrite pour des versions bien plus anciennes. Elle appelle les méthodes de l'objet `qtile` avec leur ancien préfixe `cmd_` (`qtile.cmd_spawn`, `qtile.cmd_to_screen`, `qtile.cmd_restart`). Depuis qtile 0.23, les commandes s'appellent sans ce préfixe (`qtile.spawn`, `qtile.to_screen`, `qtile.restart`) et les alias `cmd_*` étaient seulement dépréciés. En 0.34 ils existent encore ; en 0.37 ils ont disparu.

Le hook `screen_change` de `.config/qtile/qtile_config/hooks.py` est par ailleurs cassé sur les deux versions :
- il est déclaré sans paramètre, alors que Qtile lui passe l'événement ;
- il appelle `qtile.cmd_restart()` alors que `qtile` n'est défini nulle part dans ce module.

Il n'a donc jamais redémarré Qtile. La reconfiguration des écrans est assurée par Qtile lui-même : `reconfigure_screens` vaut `True` par défaut, et la config ne le redéfinit pas.

## Problème

- **Symptôme** : sur le laptop, les raccourcis qui lancent un script ne font rien. Le log de Qtile montre :
  ```
  File "/home/fabien/.config/qtile/qtile_config/keybindings.py", line 20, in run_prompt
      qtile.cmd_spawn(command.run)
  AttributeError: 'Qtile' object has no attribute 'cmd_spawn'. Did you mean: 'no_spawn'?
  ```
  À chaque changement d'écran, le log montre aussi :
  ```
  ERROR libqtile hook.py:fire() Error in hook screen_change
  TypeError: screen_change() takes 0 positional arguments but 1 was given
  ```
- **Déclencheur** : qtile ≥ 0.37 (alias `cmd_*` retirés) ; pour le hook, n'importe quelle version, à chaque événement `screen_change`.
- **Impact** : sur le laptop, sept fonctions de `keybindings.py` échouent :
  - le menu run (`run_prompt`) ;
  - le choix du thème (`pick_theme`) ;
  - les quatre presets de layout d'écran ;
  - le changement d'écran avec notification (`toggle_screen_focus`).

  Sur les deux machines, le log reçoit une erreur à chaque changement d'écran.

## Comportement attendu

1. Toutes les fonctions de `keybindings.py` marchent à l'identique en qtile 0.34 et 0.37.
2. Plus aucun appel `qtile.cmd_*` dans le code chargé par Qtile (`.config/qtile/config.py` et `.config/qtile/qtile_config/`).
3. Plus aucune erreur `screen_change` dans le log. Le comportement réel ne change pas : la reconfiguration des écrans reste celle de Qtile (`reconfigure_screens`, valeur par défaut).
4. `bin/powermenu.sh` n'appelle plus `qtile-cmd`, un binaire retiré de qtile depuis longtemps.

> Invariant : la même config doit tourner sur les deux machines. Aucun test de version, aucune branche `if version`.

## Comportement actuel (avant fix)

- qtile 0.37, raccourci du menu run (`run_prompt`) → `AttributeError: 'Qtile' object has no attribute 'cmd_spawn'`, rien ne s'ouvre.
- qtile 0.37, raccourcis `set_vertical_monitor_layout`, `set_horizontal_monitor_layout`, `set_samsung_monitor_layout`, `set_samsung_monitor_dual_layout`, `pick_theme` → même `AttributeError`.
- qtile 0.37, `toggle_screen_focus` → `AttributeError` sur `cmd_spawn`, donc ni notification, ni `cmd_to_screen`, ni déplacement du curseur.
- qtile 0.34 et 0.37, branchement ou débranchement d'un écran → `TypeError` dans le hook `screen_change`.
- qtile 0.34 : les raccourcis marchent, mais avec les alias dépréciés.

## Cause identifiée

- `.config/qtile/qtile_config/keybindings.py` — huit appels à des alias `cmd_*` retirés en 0.37 :
  - `qtile.cmd_spawn` aux lignes 16, 20, 24, 28, 32, 36 et 51 ;
  - `qtile.cmd_to_screen` à la ligne 53.
- `.config/qtile/qtile_config/hooks.py` (lignes 13-15) — `screen_change()` sans paramètre, et `qtile` non défini dans le module.
- `.config/qtile/bin/powermenu.sh` (ligne 18) — `qtile-cmd -o cmd -f shutdown`, binaire disparu (remplacé par `qtile cmd-obj`).

## Solution

### `keybindings.py`

Remplacer chaque alias par la commande sans préfixe, avec les mêmes arguments :
- `qtile.cmd_spawn(...)` → `qtile.spawn(...)` ;
- `qtile.cmd_to_screen(...)` → `qtile.to_screen(...)`.

Ces noms existent en 0.34 comme en 0.37 : une seule écriture pour les deux machines.

### `hooks.py`

Supprimer le hook `screen_change` (lignes 13-15). Il n'a jamais fonctionné, et Qtile reconfigure déjà les écrans de lui-même (`reconfigure_screens = True` par défaut). Le corriger pour qu'il redémarre réellement Qtile changerait le comportement : un redémarrage complet à chaque événement d'écran, avec un risque de boucle. Les imports devenus inutiles éventuels sont laissés tels quels (hors périmètre).

### `bin/powermenu.sh`

`qtile-cmd -o cmd -f shutdown` → `qtile cmd-obj -o cmd -f shutdown`, la forme déjà utilisée par `bin/theme/pick`.

### Documentation

Dans `.config/qtile/CLAUDE.md`, une ligne sous « Keybinding Conventions » : appeler les commandes de l'objet `qtile` sans préfixe `cmd_` (`qtile.spawn`, `qtile.to_screen`, `qtile.restart`), compatibles 0.34 et 0.37.

## Contraintes à respecter

- Une seule config pour 0.34 et 0.37 : aucun test de version.
- Aucun autre changement de comportement : mêmes raccourcis, mêmes commandes lancées, mêmes arguments.
- Ne pas toucher à `.config/qtile/test_widget_network.py` : brouillon non chargé par Qtile, hors périmètre (il contient aussi des `cmd_spawn`).
- Ne pas définir `reconfigure_screens` dans la config : la valeur par défaut de Qtile fait le travail.
- Les commits suivent `## Commits` du `CLAUDE.md`.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`), et Qtile n'est pas installé dans le container : il n'y a pas de fichier de test à écrire. Les vérifications se font par commande dans la session, puis à la main par l'humain sur ses deux machines.

| Cas | Attendu |
|-----|---------|
| `grep -rn "cmd_" .config/qtile/qtile_config .config/qtile/config.py` | aucun résultat (reproduit le bug avant fix : 9 résultats) |
| `grep -n "qtile-cmd" .config/qtile/bin/powermenu.sh` | aucun résultat |
| `grep -n "screen_change" .config/qtile/qtile_config/hooks.py` | aucun résultat |
| `python3 -m py_compile .config/qtile/qtile_config/*.py` ; `bash -n .config/qtile/bin/powermenu.sh` | aucune erreur |
| Laptop (0.37) — `qtile check -c ~/.config/qtile/config.py` | aucune erreur |
| Laptop (0.37) — raccourci du menu run | rofi s'ouvre ; plus d'`AttributeError` dans `~/.local/share/qtile/qtile.log` |
| Laptop (0.37) — raccourci du choix de thème, puis `toggle_screen_focus` | le menu des thèmes s'ouvre ; la notification « focused … screen » apparaît et le focus change d'écran |
| Laptop (0.37) — brancher / débrancher un écran | aucune erreur `screen_change` dans le log, les écrans sont reconfigurés |
| Poste fixe (0.34) — mêmes raccourcis | comportement inchangé, aucune erreur dans le log |
