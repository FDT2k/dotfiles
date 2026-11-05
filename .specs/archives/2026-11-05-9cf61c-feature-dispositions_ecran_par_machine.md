# Dispositions d'écran par machine : {hostname}.sh par défaut, variantes {hostname}_{nom}.sh et menu rofi

Status: implemented
Chantier: divers

## Situation initiale

> Cette spec s'implémente **après** `8d134c` (nettoyage des écrans) et `861406` (groupe `sddm`). Elle part de l'état qu'elles laissent.

Après `8d134c`, `.config/qtile/bin/screenlayout.d/` ne contient plus que :
- `daoloth.sh` : la disposition xrandr du poste fixe (`DisplayPort-4/5/6/7`) ;
- `sddm` : un lien symbolique vers `daoloth.sh` ;
- `arandr` : il lance l'éditeur graphique.

Le menu « Monitor Layout » (`Key([mod, alt], "l", lazy.spawn(command.screen_layout))`, `command.screen_layout` = `bin/run.sh screenlayout.d "Monitor Layout"`) liste **tous** les fichiers du dossier dans rofi et exécute celui choisi.

Après `861406`, SDDM lance `~/.config/qtile/bin/screenlayout.d/sddm` avant l'écran de login (`/etc/sddm.conf.d/10-dotfiles.conf`, `[X11] DisplayCommand`). Ce lien pointe vers la disposition du fixe, y compris sur le laptop.

`.config/qtile/autostart.sh` ne règle pas les écrans.

Machines actuelles : le fixe **daoloth** et le laptop **abhoth**. Les deux reçoivent des écrans portables : il faut plusieurs dispositions par machine.

## Besoin

- **Qui** : l'humain, sur ses deux machines.
- **Quoi** :
  - pour chaque machine, une disposition par défaut et autant de variantes que nécessaire (écran portable branché, etc.) ;
  - un menu qui ne montre que celles de la machine courante ;
  - la disposition par défaut appliquée avant le login (SDDM) et au démarrage de la session.
- **Pourquoi** : changer de disposition en deux touches selon les écrans branchés, et avoir les bons écrans dès le démarrage sur chaque machine, sans réglage propre à une seule machine dans le code.

## Spécification fonctionnelle

### Règles métier

Aucune business rule : le dépôt n'a pas de `.specs/docs/business_rules/`.

Décisions de l'humain :
- dispositions nommées par **hostname** ;
- le menu ne montre que la **machine courante** ;
- SDDM lance la disposition par défaut de la machine ;
- la disposition par défaut est **aussi appliquée par `autostart.sh`**.

Règles :
1. **Convention de nommage** dans `screenlayout.d/` :
   - `{hostname}.sh` : disposition **par défaut** de la machine ;
   - `{hostname}_{nom}.sh` : variante `{nom}` (lettres, chiffres, `-`) ;
   - le hostname vient de **`uname -n`**, et non de `hostname`, qui n'est pas forcément installé sur Arch.
2. **Nouveau script `.config/qtile/bin/screenlayout`** :
   - **sans argument**, il ouvre un menu rofi (`-dmenu -p "Monitor Layout"`) qui liste, dans cet ordre :
     - `default`, si `{hostname}.sh` existe ;
     - chaque `{nom}` des `{hostname}_{nom}.sh`, par ordre alphabétique ;
     - `arandr`.

     Le choix lance le script correspondant. Menu annulé → rien.
   - **`--default`** : lance `{hostname}.sh` s'il existe et est exécutable, sans menu ; sinon il ne fait rien, en code 0.
   - Il ne liste jamais les fichiers d'une autre machine, ni `sddm`.
3. **`screenlayout.d/sddm`** : le lien vers `daoloth.sh` est remplacé par un **script** exécutable `#!/bin/sh` qui lance `../screenlayout --default`. Le chemin est résolu depuis l'emplacement réel du script (`readlink -f "$0"`). Le chemin vu par SDDM ne change donc pas, et chaque machine applique sa propre disposition par défaut.
4. **`autostart.sh`** lance `$DIR/bin/screenlayout --default`, en premier et de façon synchrone (pas de `&`), avant `bin/theme/reload`, pour que le fond d'écran soit posé sur les bons écrans.
5. **`commands.py`** : `screen_layout` pointe vers `../bin/screenlayout`. Le raccourci `mod+alt+l` ne change pas.
6. `daoloth.sh` et `abhoth.sh` (écran interne `eDP-1` en 1920x1200, ajouté par l'humain) restent tels quels : ce sont déjà les `{hostname}.sh` des deux machines. Les variantes s'ajoutent par exemple avec arandr (« Enregistrer sous… » `{hostname}_{nom}.sh` dans `screenlayout.d/`).

### Parcours utilisateur

1. Au démarrage, SDDM lance `screenlayout.d/sddm`, donc `{hostname}.sh` (daoloth : `daoloth.sh` ; abhoth : `abhoth.sh`).
2. À l'ouverture de la session, `autostart.sh` relance `{hostname}.sh`.
3. L'humain branche un écran portable, tape `mod+alt+l` et choisit, par exemple, `portable` : `daoloth_portable.sh` s'exécute. Qtile reconfigure ses écrans de lui-même.
4. Il peut revenir à `default`, ou ouvrir `arandr` pour créer une nouvelle variante.

## Edge cases

| Situation | Comportement attendu |
|-----------|---------------------|
| Machine sans `{hostname}.sh` (machine inconnue) | menu sans `default` (variantes éventuelles + `arandr`) ; `--default`, SDDM et autostart ne font rien, sans erreur |
| Fichier `{hostname}_{nom}.sh` non exécutable | non listé |
| Hostname contenant `_` | hors périmètre : daoloth et abhoth n'en ont pas |
| Fichiers d'une autre machine (`abhoth*.sh` sur daoloth) | jamais listés ni lancés |
| `{hostname}.sh` en échec (sortie absente) | code de retour non nul, ignoré par autostart (qui continue) ; SDDM continue vers le login |
| Menu annulé | rien n'est lancé |
| Entrée `sddm` ou autre fichier hors convention dans le dossier | ignoré par le menu |

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

| Fichier | Rôle |
|---------|------|
| `.config/qtile/bin/screenlayout` | menu rofi des dispositions de la machine courante, et `--default` |

### Fichiers à modifier

| Fichier | Modification |
|---------|-------------|
| `.config/qtile/bin/screenlayout.d/sddm` | lien symbolique → script exécutable qui lance `../screenlayout --default` |
| `.config/qtile/qtile_config/commands.py` | `screen_layout` → `../bin/screenlayout` |
| `.config/qtile/autostart.sh` | `$DIR/bin/screenlayout --default` en premier, synchrone |
| `.config/qtile/bin/screenlayout.d/daoloth.sh` | commentaire en tête **remplaçant** celui posé par `861406` (pas un second) : disposition par défaut de daoloth (convention `{hostname}.sh`), lancée par SDDM et autostart ; même commentaire adapté en tête de `abhoth.sh` |
| `.config/qtile/CLAUDE.md` | section « Monitor Configuration » : convention de nommage, script `screenlayout`, SDDM et autostart |
| `CLAUDE.md` | une ligne dans la partie Qtile : dispositions d'écran par hostname dans `bin/screenlayout.d/` |

## Contraintes à respecter

- Ne pas modifier le contenu xrandr de `daoloth.sh`.
- Ne pas modifier `bin/run.sh` : les autres menus `.d` l'utilisent toujours.
- Le chemin `screenlayout.d/sddm` vu par SDDM ne change pas (aucune intervention sur `/etc/sddm.conf.d/`).
- Ne modifier ni `daoloth.sh` ni `abhoth.sh` ; ne créer aucune variante.
- `hostname` n'est jamais appelé : `uname -n` seulement.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Les cas se jouent avec un dossier de test, de faux `uname`, `rofi` et des scripts de disposition qui écrivent dans un journal, puis sur les deux machines.

| Cas | Attendu |
|-----|---------|
| `bash -n` sur `screenlayout`, `screenlayout.d/sddm`, `autostart.sh` | aucune erreur |
| Faux `uname -n` = `daoloth`, fichiers `daoloth.sh`, `daoloth_portable.sh`, `daoloth_tv.sh`, `abhoth.sh`, `sddm` | menu reçoit exactement `default`, `portable`, `tv`, `arandr` |
| Choix `portable` | `daoloth_portable.sh` exécuté |
| Choix `default` / `arandr` | `daoloth.sh` / `arandr` exécuté |
| Menu annulé (rofi renvoie vide) | rien exécuté, code 0 |
| `screenlayout --default` sur daoloth | `daoloth.sh` exécuté, sans rofi |
| Faux `uname -n` = `abhoth` | menu : `default`, `arandr` (plus les variantes `abhoth_*` si présentes) ; `--default` lance `abhoth.sh` |
| Faux `uname -n` = `inconnu`, sans `inconnu.sh` | `--default` : rien, code 0 ; menu : `arandr` seul |
| `daoloth_x.sh` non exécutable | non listé |
| `screenlayout.d/sddm` lancé depuis un autre dossier courant | exécute `screenlayout --default` (chemin résolu par `readlink -f`) |
| `git ls-files -s .config/qtile/bin/screenlayout.d/sddm` | mode `100755` (script), plus `120000` |
| `autostart.sh` | `screenlayout --default` appelé avant `theme/reload` |
| Fixe — `mod+alt+l` | menu `default` + `arandr` (et les variantes ajoutées) |
| Laptop — démarrage | `abhoth.sh` appliqué au login et à l'ouverture de session |
