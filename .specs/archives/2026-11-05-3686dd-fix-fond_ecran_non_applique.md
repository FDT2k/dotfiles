# Le fond d'écran n'est plus posé depuis le passage à hellwal

Status: implemented
Chantier: divers

## Situation initiale

Avec pywal, `wal -i <image>` faisait deux choses à la fois :
- générer la palette ;
- **poser le fond d'écran**, en appelant le premier outil disponible sur la machine (feh, xwallpaper, nitrogen…).

Les dotfiles ne posaient donc jamais le fond eux-mêmes :
- aucun appel à feh, xwallpaper ou nitrogen ;
- le `feh --bg-fill` d'`.config/qtile/autostart.sh` (ligne 49) est commenté ;
- les `Screen()` de `.config/qtile/qtile_config/screens.py` n'ont pas d'option `wallpaper`.

La spec `0da46c` ([archive](./2026-11-05-0da46c-change-pywal_vers_hellwal.md)) a remplacé `wal -i` par `hellwal-apply`. hellwal génère les couleurs, les templates et la recoloration des terminaux, mais **ne pose pas le fond d'écran**. La spec n'avait pas relevé ce second rôle de `wal -i`.

Le chemin de l'image est pourtant disponible : le template `.config/hellwal/templates/colors.json` écrit `"wallpaper": "%%wallpaper%%"` (chemin absolu, via le `realpath` de `hellwal-apply`). `.config/qtile/qtile_config/themes.py` le lit déjà, dans la variable `wallpaper`, sans s'en servir.

## Problème

- **Symptôme** : sur le laptop, un changement de thème change les couleurs, pas le fond d'écran.
- **Déclencheur** : tout changement de thème (`bin/theme/pick`) et tout démarrage de Qtile, depuis le passage à hellwal.
- **Impact** : le fond reste celui d'avant (ou noir sur une machine neuve), décorrélé des couleurs générées depuis l'image. Le poste fixe aura le même défaut dès qu'il passera à hellwal.

## Comportement attendu

1. Qtile pose lui-même le fond d'écran sur **chaque écran** déclaré dans `screens.py`, avec l'image de `colors.json` en mode `fill`.
2. Après un changement de thème, le fond suit l'image choisie. `pick` redémarre déjà Qtile après `hellwal-apply`, et Qtile relit `colors.json` au démarrage.
3. `colors.json` absent ou inutilisable (palette par défaut de `themes.py`), ou image introuvable → **aucun fond posé par Qtile**, et Qtile démarre normalement.
4. Aucun paquet supplémentaire : pas de feh ni de xwallpaper.

> Invariants : même config pour qtile 0.34 (poste fixe) et 0.37 (laptop) ; barres, widgets et nombre d'écrans inchangés.

## Comportement actuel (avant fix)

- Changement de thème depuis Qtile → couleurs mises à jour, fond d'écran inchangé.
- Laptop neuf → fond noir (ou celui du gestionnaire de connexion), quel que soit le thème.

## Cause identifiée

- `.config/qtile/qtile_config/screens.py` (lignes 10-98) — les quatre `Screen()` ne reçoivent ni `wallpaper` ni `wallpaper_mode` ; le fond reposait implicitement sur `wal -i`.
- `.config/qtile/qtile_config/themes.py` (ligne 42) — `wallpaper` est lu mais n'est utilisé nulle part.

## Solution

### `screens.py`

Importer `wallpaper` depuis `.themes`. Construire une seule fois les arguments de fond :
- `{'wallpaper': wallpaper, 'wallpaper_mode': 'fill'}` si `wallpaper` est non vide et que `os.path.isfile(wallpaper)` est vrai ;
- sinon `{}`.

Les passer (`**wallpaper_args`) aux **quatre** `Screen(...)` existants : le premier, avec sa barre, et les trois `Screen()` vides. Aucun autre argument ne change.

### Documentation

- **`CLAUDE.md`** (bullet Thème) : le fond d'écran est posé par Qtile (`screens.py`, `wallpaper_mode='fill'`) à partir du chemin `wallpaper` de `colors.json`. hellwal ne le pose pas.
- **`.config/qtile/CLAUDE.md`** (Color/Theme System) : la même information.

## Contraintes à respecter

- Pas de feh, xwallpaper ni autre outil : c'est Qtile qui pose le fond.
- Ne pas toucher à `hellwal-apply`, `pick`, `reload` ni aux templates.
- Ne pas décommenter le `feh` d'`autostart.sh`.
- `themes.py` reste la seule lecture de `colors.json` ; `screens.py` ne fait que consommer `wallpaper`.
- `install-arch-deps.sh` n'est pas modifié : aucun paquet nouveau.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`) et Qtile n'est pas installé dans le container. Les vérifications se font avec une fausse `libqtile` minimale (classes `Screen`, `bar.Bar`, widgets enregistrant leurs arguments), puis à la main sur le laptop.

| Cas | Attendu |
|-----|---------|
| `python3 -m py_compile .config/qtile/qtile_config/*.py` | aucune erreur |
| Reproduit le bug — avant fix, `screens.py` chargé avec un `colors.json` valide | aucun `Screen` ne reçoit `wallpaper` |
| Après fix, `colors.json` valide, image existante | les 4 `Screen` reçoivent `wallpaper=<chemin>` et `wallpaper_mode='fill'` |
| Après fix, `colors.json` absent (palette par défaut) | aucun `Screen` ne reçoit `wallpaper`, le module se charge |
| Après fix, `colors.json` valide mais image supprimée | aucun `Screen` ne reçoit `wallpaper`, le module se charge |
| Après fix, le premier `Screen` | garde sa barre `top` et ses arguments inchangés |
| Laptop (0.37) — changement de thème depuis Qtile | après le redémarrage, le fond est l'image choisie, sur chaque écran |
| Poste fixe (0.34), une fois passé à hellwal — même geste | même résultat |
