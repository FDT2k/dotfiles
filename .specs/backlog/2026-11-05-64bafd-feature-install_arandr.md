# Ajouter arandr au script d'installation

Status: draft
Chantier: divers

## Situation initiale

`.config/qtile/bin/install-arch-deps.sh` installe ses paquets par groupes : `rofi`, `theme`, `lock`, `dunst`, `terminator`. Sans argument, il installe tous les groupes. Il passe uniquement par `sudo pacman -S --needed`, dans les dépôts officiels, et compile les outils non packagés avec `git_install`.

Le menu des dispositions d'écran (`bin/run.sh screenlayout.d "Monitor Layout"`, raccourci `command.screen_layout` de `qtile_config/commands.py`) propose une entrée `arandr` (`.config/qtile/bin/screenlayout.d/arandr`). Elle lance l'éditeur graphique de disposition d'écrans. Les autres entrées du menu, et les scripts de `bin/monitor_layout/`, appellent `xrandr`.

arandr n'est installé par aucun groupe. Sur une machine neuve, l'entrée `arandr` du menu ne fait rien.

## Besoin

- **Qui** : l'humain, en installant une machine.
- **Quoi** : que le script d'installation installe arandr.
- **Pourquoi** : l'entrée `arandr` du menu des dispositions d'écran doit marcher sur toute machine installée avec le script.

## Spécification fonctionnelle

### Règles métier

Aucune business rule : le dépôt n'a pas de `.specs/docs/business_rules/`.

1. Un nouveau groupe **`screens`** installe `arandr` et `xorg-xrandr` : l'éditeur graphique, et `xrandr`, utilisé par les autres entrées du menu et par `bin/monitor_layout/`.
2. `screens` fait partie des groupes installés par défaut (sans argument), après `terminator`.
3. `install-arch-deps.sh screens` installe ce groupe seul.
4. Le message de groupe inconnu et l'en-tête du script listent `screens`.
5. Les paquets en double entre groupes ne sont installés qu'une fois (`xorg-xrandr` est aussi dans `lock`) : c'est déjà le cas grâce à la déduplication existante.

### Parcours utilisateur

1. L'humain lance `~/.config/qtile/bin/install-arch-deps.sh` (ou `… screens`).
2. pacman installe `arandr` et `xorg-xrandr` s'ils manquent.
3. L'entrée `arandr` du menu « Monitor Layout » ouvre arandr.

## Edge cases

| Situation | Comportement attendu |
|-----------|---------------------|
| `screens` et `lock` demandés ensemble | `xorg-xrandr` une seule fois dans la commande pacman |
| arandr déjà installé | sauté par `--needed` |
| Groupe inconnu | message listant `rofi, theme, lock, dunst, terminator, screens`, code 2 |

## Conception technique

### Migrations schéma

Aucune

### Migrations données

Aucune

### Actions / Listeners

Sans objet.

### Panel / UI (Filament)

Sans objet.

### Fichiers à créer

Aucun.

### Fichiers à modifier

| Fichier | Modification |
|---------|-------------|
| `.config/qtile/bin/install-arch-deps.sh` | tableau `SCREENS_PKGS=(arandr xorg-xrandr)` commenté, cas `screens` du `case`, groupes par défaut, message de groupe inconnu, en-tête |
| `.config/qtile/CLAUDE.md` | groupe `screens` dans la ligne d'usage du script |

## Contraintes à respecter

- Dépôts officiels seulement ; aucun AUR.
- Les autres groupes et `git_install` ne changent pas.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Les cas se jouent avec un faux `sudo` et un `HOME` de test, comme pour les ajouts précédents.

| Cas | Attendu |
|-----|---------|
| `bash -n .config/qtile/bin/install-arch-deps.sh` | aucune erreur |
| Sans argument | `arandr` et `xorg-xrandr` dans la commande pacman, `xorg-xrandr` une seule fois |
| `install-arch-deps.sh screens` | commande pacman : `arandr xorg-xrandr` seulement, aucun appel git |
| `install-arch-deps.sh screens lock` | `xorg-xrandr` une seule fois |
| `install-arch-deps.sh foo` | message listant `screens`, code 2 |
