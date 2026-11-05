# Groupe sddm du script d'installation : brancher SDDM sur la disposition d'écrans

Status: draft
Chantier: divers

## Situation initiale

Sur le poste fixe (daoloth), l'écran de connexion SDDM règle les écrans avant d'afficher le login. L'humain a modifié à la main `/usr/share/sddm/scripts/Xsetup` :

```sh
#!/bin/sh
# Xsetup - run as root before the login dialog appears
source /home/fabien/.config/qtile/bin/screenlayout.d/sddm
```

`.config/qtile/bin/screenlayout.d/sddm` est un **lien symbolique versionné** vers `daoloth.sh` (même dossier, exécutable, `#!/bin/sh`). Ce script fait un `xrandr` sur les sorties du fixe : `DisplayPort-4/5/6/7`.

Ce réglage est fragile et non reproductible :
- `/usr/share/sddm/scripts/Xsetup` appartient au paquet `sddm`, et une mise à jour peut l'écraser ;
- rien dans les dotfiles ne le recrée sur une nouvelle installation.

SDDM lit sa configuration dans `/etc/sddm.conf` et les fichiers de `/etc/sddm.conf.d/`. La clé `[X11] DisplayCommand` désigne le script lancé, en root, avant le login. Elle vaut `/usr/share/sddm/scripts/Xsetup` par défaut.

`.config/qtile/bin/install-arch-deps.sh` installe des groupes de paquets par `sudo pacman -S --needed`, dans les dépôts officiels uniquement (`rofi`, `theme`, `lock`, `dunst`, `terminator`, `screens`, `fonts`, tous installés par défaut).

## Besoin

- **Qui** : l'humain, en installant ou en réinstallant une machine.
- **Quoi** : que le script d'installation installe SDDM et le branche sur `screenlayout.d/sddm`, sans retoucher à la main un fichier du paquet.
- **Pourquoi** : rendre le réglage de l'écran de login reproductible, et le protéger des mises à jour de `sddm`.

## Spécification fonctionnelle

### Règles métier

Aucune business rule : le dépôt n'a pas de `.specs/docs/business_rules/`.

Décisions de l'humain :
- configuration par `/etc/sddm.conf.d/`, pas en réécrivant `Xsetup` ;
- le setup vit dans un groupe `sddm` d'`install-arch-deps.sh` ;
- pas de logique par machine pour l'instant : on fait juste le script d'installation.

Règles :
1. Nouveau groupe **`sddm`** dans `install-arch-deps.sh`, **absent des groupes par défaut** : il ne s'installe que par `install-arch-deps.sh sddm`. Il touche à la configuration système, et toutes les machines n'utilisent pas SDDM.
2. Le groupe installe le paquet `sddm` (`pacman --needed`).
3. Après pacman, le script écrit avec `sudo` le fichier **`/etc/sddm.conf.d/10-dotfiles.conf`** :
   ```ini
   # Written by ~/.config/qtile/bin/install-arch-deps.sh (group sddm)
   [X11]
   DisplayCommand=<HOME>/.config/qtile/bin/screenlayout.d/sddm
   ```
   `<HOME>` est le `$HOME` de l'utilisateur qui lance le script, développé à l'écriture. Le fichier est en `root:root`, mode `644`. Le dossier `/etc/sddm.conf.d/` est créé s'il manque.
4. Le fichier est **réécrit à chaque lancement** du groupe : son contenu ne dépend que du `$HOME`.
5. Si `~/.config/qtile/bin/screenlayout.d/sddm` n'existe pas ou n'est pas exécutable (lien cassé compris), le script **avertit** sans échouer : `==> warning: <chemin> missing or not executable: SDDM will run it before the login screen`.
6. `/usr/share/sddm/scripts/Xsetup` n'est **jamais** touché. Le script affiche une ligne qui rappelle qu'une ligne `source …` ajoutée à la main dans `Xsetup` n'est plus utile, et qu'elle peut être retirée ou laissée.
7. Le script n'active pas le service (`systemctl enable sddm`) : c'est un geste de l'humain, signalé par une ligne `==> sddm: enable it with: sudo systemctl enable sddm` si `systemctl is-enabled sddm` ne répond pas `enabled`.

### Parcours utilisateur

1. L'humain lance `~/.config/qtile/bin/install-arch-deps.sh sddm` sur le fixe.
2. pacman installe `sddm` s'il manque.
3. Le script écrit `/etc/sddm.conf.d/10-dotfiles.conf`, qui pointe vers `~/.config/qtile/bin/screenlayout.d/sddm`.
4. Au prochain démarrage, SDDM lance ce script, donc `daoloth.sh`, avant le login.

## Edge cases

| Situation | Comportement attendu |
|-----------|---------------------|
| `install-arch-deps.sh` sans argument | groupe `sddm` **non** installé, aucun `sudo` vers `/etc/sddm.conf.d/` |
| `/etc/sddm.conf.d/` absent | créé par `sudo mkdir -p` |
| `10-dotfiles.conf` déjà présent | réécrit avec le contenu courant |
| `screenlayout.d/sddm` absent ou lien cassé | avertissement, fichier de conf écrit quand même, code 0 |
| SDDM non activé | ligne rappelant `sudo systemctl enable sddm`, rien n'est activé |
| `Xsetup` modifié à la main (cas du fixe) | non touché ; ligne de rappel affichée |
| Groupe inconnu | message listant aussi `sddm`, code 2 |
| Comportement sur le laptop (sorties différentes) | hors périmètre : le lien `sddm` pointe vers la disposition du fixe ; la logique par machine viendra plus tard |

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

Aucun dans le dépôt : `/etc/sddm.conf.d/10-dotfiles.conf` est écrit sur la machine par le script.

### Fichiers à modifier

| Fichier | Modification |
|---------|-------------|
| `.config/qtile/bin/install-arch-deps.sh` | `SDDM_PKGS=(sddm)` commenté ; cas `sddm` du `case` (hors groupes par défaut) ; fonction `setup_sddm` (écriture de la conf, avertissements, rappels) ; message de groupe inconnu et en-tête |
| `.config/qtile/bin/screenlayout.d/daoloth.sh` | commentaire en tête : lancé aussi par SDDM avant le login via le lien `sddm` et `/etc/sddm.conf.d/10-dotfiles.conf` ; ne pas renommer le lien `sddm` |
| `.config/qtile/CLAUDE.md` | groupe `sddm` dans la ligne d'usage, en précisant qu'il n'est pas installé par défaut |
| `CLAUDE.md` | une ligne dans « Divers » : SDDM lance `screenlayout.d/sddm` par `/etc/sddm.conf.d/10-dotfiles.conf`, posé par `install-arch-deps.sh sddm` |

## Contraintes à respecter

- Dépôts officiels seulement.
- Ne jamais écrire dans `/usr/share/sddm/`.
- Ne pas activer ni redémarrer SDDM.
- Ne pas modifier le lien `screenlayout.d/sddm` ni le contenu `xrandr` de `daoloth.sh`.
- Hors périmètre : le nettoyage de `screenlayout.d/` (spec séparée), le thème SDDM (`bin/theme/sddm`), la logique par machine.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Les cas se jouent avec un `HOME` de test et des faux `sudo`, `pacman` et `systemctl`. Le faux `sudo` exécute la commande en redirigeant `/etc/sddm.conf.d` vers un dossier de test, grâce à une variable `SDDM_CONF_DIR` (défaut `/etc/sddm.conf.d`) que le script expose pour ça. La vérification réelle se fait sur le fixe.

| Cas | Attendu |
|-----|---------|
| `bash -n install-arch-deps.sh` | aucune erreur |
| Sans argument | commande pacman sans `sddm` ; aucun fichier écrit dans le dossier de conf de test |
| `install-arch-deps.sh sddm` | pacman reçoit `sddm` ; `10-dotfiles.conf` contient `[X11]` et `DisplayCommand=$HOME/.config/qtile/bin/screenlayout.d/sddm` (chemin développé) |
| Relance | fichier réécrit, contenu identique |
| `screenlayout.d/sddm` absent du `HOME` de test | avertissement `missing or not executable`, code 0, fichier écrit |
| Faux `systemctl is-enabled sddm` → `disabled` | ligne `enable it with: sudo systemctl enable sddm` ; aucun `systemctl enable` lancé |
| Aucun accès à `/usr/share/sddm` | vérifié : aucune commande ne le mentionne hors du message de rappel |
| `install-arch-deps.sh foo` | message listant `sddm`, code 2 |
| Fixe — `install-arch-deps.sh sddm`, puis redémarrage | écrans réglés avant le login, comme aujourd'hui |
