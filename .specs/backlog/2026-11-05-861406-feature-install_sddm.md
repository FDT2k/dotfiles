# Groupe sddm du script d'installation : disposition d'écrans et thème fdt2k-dark

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

**Thème.** Le thème SDDM de l'humain, `fdt2k-dark`, a été copié à la main dans `/usr/share/sddm/themes/fdt2k-dark/`. Il est choisi par `/etc/sddm.conf.d/sddm.conf` (`[Theme] Current=fdt2k-dark`), écrit lui aussi à la main. Il est désormais versionné dans `.local/share/sddm/themes/fdt2k-dark/`, avec `theme.conf.user`. Ce fichier est **généré** : `.config/qtile/bin/theme/sddm` le réécrit à chaque changement de thème (lancé par `bin/theme/pick`), dans `/usr/share/sddm/themes/fdt2k-dark/theme.conf.user`. Il y écrit `background=/home/fabien/.cache/wal/current-theme.jpg` et les couleurs `BackgroundColor`, `MainColor`, `AccentColor` tirées de `~/.cache/wal/colors`.

L'écran de login tourne sous l'utilisateur système **`sddm`**. Pour lire un thème ou un fond situé dans le home, il doit pouvoir traverser les dossiers parents. Constaté par l'humain :

| Machine | `~` | `~/.local` | `~/.local/share` |
|---|---|---|---|
| fixe (daoloth) | 755 | 755 | 755 |
| laptop (abhoth) | **700** | 755 | 755 |

`.config/qtile/bin/install-arch-deps.sh` installe des groupes de paquets par `sudo pacman -S --needed`, dans les dépôts officiels uniquement (`rofi`, `theme`, `lock`, `dunst`, `terminator`, `screens`, `fonts`, tous installés par défaut).

## Besoin

- **Qui** : l'humain, en installant ou en réinstallant une machine.
- **Quoi** : que le script d'installation installe SDDM, le branche sur `screenlayout.d/sddm` et installe le thème `fdt2k-dark` depuis les dotfiles, sans retoucher à la main un fichier du paquet.
- **Pourquoi** : rendre le réglage de l'écran de login reproductible, et le protéger des mises à jour de `sddm`.

## Spécification fonctionnelle

### Règles métier

Aucune business rule : le dépôt n'a pas de `.specs/docs/business_rules/`.

Décisions de l'humain :
- configuration par `/etc/sddm.conf.d/`, pas en réécrivant `Xsetup` ;
- le setup vit dans un groupe `sddm` d'`install-arch-deps.sh` ;
- pas de logique par machine pour l'instant : on fait juste le script d'installation ;
- le thème est installé par un **lien symbolique** vers les dotfiles ;
- si l'utilisateur `sddm` ne peut pas lire le home (laptop en 700), le script **avertit** et donne la commande à lancer, **sans changer les droits lui-même**.

Règles :
1. Nouveau groupe **`sddm`** dans `install-arch-deps.sh`, **absent des groupes par défaut** : il ne s'installe que par `install-arch-deps.sh sddm`. Il touche à la configuration système, et toutes les machines n'utilisent pas SDDM.
2. Le groupe installe le paquet `sddm` (`pacman --needed`).
3. Après pacman, le script écrit avec `sudo` le fichier **`/etc/sddm.conf.d/10-dotfiles.conf`** :
   ```ini
   # Written by ~/.config/qtile/bin/install-arch-deps.sh (group sddm)
   [Theme]
   Current=fdt2k-dark

   [X11]
   DisplayCommand=<HOME>/.config/qtile/bin/screenlayout.d/sddm
   ```
   `<HOME>` est le `$HOME` de l'utilisateur qui lance le script, développé à l'écriture. Le fichier est en `root:root`, mode `644`. Le dossier `/etc/sddm.conf.d/` est créé s'il manque.
4. Le fichier est **réécrit à chaque lancement** du groupe : son contenu ne dépend que du `$HOME`.
5. Si `~/.config/qtile/bin/screenlayout.d/sddm` n'existe pas ou n'est pas exécutable (lien cassé compris), le script **avertit** sans échouer : `==> warning: <chemin> missing or not executable: SDDM will run it before the login screen`.
6. `/usr/share/sddm/scripts/Xsetup` n'est **jamais** touché. Le script affiche une ligne qui rappelle qu'une ligne `source …` ajoutée à la main dans `Xsetup` n'est plus utile, et qu'elle peut être retirée ou laissée.
7. Le script n'active pas le service (`systemctl enable sddm`) : c'est un geste de l'humain, signalé par une ligne `==> sddm: enable it with: sudo systemctl enable sddm` si `systemctl is-enabled sddm` ne répond pas `enabled`.
8. **Thème** : `/usr/share/sddm/themes/fdt2k-dark` devient, avec `sudo`, un **lien symbolique** vers `<HOME>/.local/share/sddm/themes/fdt2k-dark` :
   - déjà ce lien → rien ;
   - un vrai dossier ou un autre lien → renommé en `fdt2k-dark.bak-<YYYYMMDD-HHMMSS>` dans le même dossier, jamais supprimé, puis le lien est posé ;
   - le dossier source des dotfiles absent → avertissement, pas de lien.
9. **Lisibilité par `sddm`** : après le lien, le script vérifie `sudo -u sddm test -r <thème>/Main.qml` et, si `~/.cache/wal/current-theme.jpg` existe, `sudo -u sddm test -r` sur ce fichier. En échec, il nomme les dossiers parents sans droit de traversée pour les autres (`o+x` absent), et affiche la commande à lancer, par exemple `chmod o+x ~ ~/.cache ~/.cache/wal`, ainsi qu'une ligne disant que SDDM retombera sinon sur son thème par défaut. Il ne lance **jamais** `chmod`.
10. **`theme.conf.user` est un fichier généré** : il est retiré du suivi git (`git rm --cached`, le fichier reste sur le disque) et ignoré par un `.gitignore` dans `.local/share/sddm/themes/fdt2k-dark/`. `bin/theme/sddm` continue d'écrire `/usr/share/sddm/themes/fdt2k-dark/theme.conf.user`, qui atterrit dans les dotfiles à travers le lien, sans `sudo`.
11. `/etc/sddm.conf.d/sddm.conf` (écrit à la main sur le fixe) n'est pas touché. Il devient redondant avec la section `[Theme]` de `10-dotfiles.conf`, et le script affiche une ligne qui le signale s'il existe.

### Parcours utilisateur

1. L'humain lance `~/.config/qtile/bin/install-arch-deps.sh sddm` sur le fixe.
2. pacman installe `sddm` s'il manque.
3. Le script écrit `/etc/sddm.conf.d/10-dotfiles.conf`, qui pointe vers `~/.config/qtile/bin/screenlayout.d/sddm`.
4. Le script pose le lien du thème et vérifie que `sddm` peut le lire ; sur le laptop, il affiche la commande `chmod o+x …` à lancer.
5. Au prochain démarrage, SDDM lance ce script, donc `daoloth.sh`, avant le login, puis affiche le thème `fdt2k-dark` avec le fond et les couleurs du thème courant.

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
| `/usr/share/sddm/themes/fdt2k-dark` est la copie à la main (cas du fixe) | renommée en `fdt2k-dark.bak-<date>`, lien posé |
| Lien déjà en place vers les dotfiles | rien n'est changé |
| `.local/share/sddm/themes/fdt2k-dark` absent des dotfiles | avertissement, pas de lien, le reste se fait |
| Home en 700 (laptop) | lien posé ; avertissement nommant `~` (et `~/.cache`, `~/.cache/wal` si besoin), commande `chmod o+x …` affichée, rien de lancé |
| Utilisateur `sddm` inexistant (paquet pas encore installé) | impossible après pacman ; si `sudo -u sddm` échoue malgré tout, avertissement « vérification impossible » |
| `/etc/sddm.conf.d/sddm.conf` présent | non touché ; ligne signalant qu'il est redondant |
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

| Fichier | Rôle |
|---------|------|
| `.local/share/sddm/themes/fdt2k-dark/.gitignore` | une ligne `theme.conf.user` |

Écrits sur la machine par le script, hors dépôt : `/etc/sddm.conf.d/10-dotfiles.conf`, le lien `/usr/share/sddm/themes/fdt2k-dark`.

### Fichiers à modifier

| Fichier | Modification |
|---------|-------------|
| `.config/qtile/bin/install-arch-deps.sh` | `SDDM_PKGS=(sddm)` commenté ; cas `sddm` du `case` (hors groupes par défaut) ; fonction `setup_sddm` (écriture de la conf, lien du thème, vérifications, avertissements, rappels) ; message de groupe inconnu et en-tête |
| `.local/share/sddm/themes/fdt2k-dark/theme.conf.user` | retiré du suivi git (`git rm --cached`), conservé sur le disque |
| `.config/qtile/bin/theme/sddm` | commentaire en tête : écrit `theme.conf.user` dans le thème, lien vers les dotfiles posé par `install-arch-deps.sh sddm` ; code inchangé |
| `.config/qtile/bin/screenlayout.d/daoloth.sh` | commentaire en tête : lancé aussi par SDDM avant le login via le lien `sddm` et `/etc/sddm.conf.d/10-dotfiles.conf` ; ne pas renommer le lien `sddm` |
| `.config/qtile/CLAUDE.md` | groupe `sddm` dans la ligne d'usage, en précisant qu'il n'est pas installé par défaut |
| `CLAUDE.md` | une ligne dans « Divers » : SDDM lance `screenlayout.d/sddm` et utilise le thème `.local/share/sddm/themes/fdt2k-dark` (lien depuis `/usr/share/sddm/themes/`), réglés par `/etc/sddm.conf.d/10-dotfiles.conf` ; tout est posé par `install-arch-deps.sh sddm` ; `theme.conf.user` est généré par `bin/theme/sddm` et ignoré |

## Contraintes à respecter

- Dépôts officiels seulement.
- Dans `/usr/share/sddm/`, ne toucher qu'à `themes/fdt2k-dark` : renommer une copie existante et poser le lien. Jamais `Xsetup`, jamais d'autre thème, jamais de suppression.
- Ne jamais lancer `chmod` ni modifier les droits du home.
- Ne pas activer ni redémarrer SDDM.
- Ne pas modifier le lien `screenlayout.d/sddm` ni le contenu `xrandr` de `daoloth.sh`.
- Ne pas modifier le contenu du thème (`Main.qml`, `theme.conf`…) ni le code de `bin/theme/sddm`.
- Hors périmètre : le nettoyage de `screenlayout.d/` (spec séparée), la logique par machine, les chemins `/home/fabien` en dur de `bin/theme/sddm`.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Les cas se jouent avec un `HOME` de test et des faux `sudo`, `pacman` et `systemctl`. Le faux `sudo` exécute la commande (en ignorant `-u sddm`, ou en simulant un refus pour les cas de lisibilité). `/etc/sddm.conf.d` et `/usr/share/sddm/themes` sont redirigés vers des dossiers de test par deux variables que le script expose pour ça : `SDDM_CONF_DIR` (défaut `/etc/sddm.conf.d`) et `SDDM_THEMES_DIR` (défaut `/usr/share/sddm/themes`). La vérification réelle se fait sur le fixe.

| Cas | Attendu |
|-----|---------|
| `bash -n install-arch-deps.sh` | aucune erreur |
| Sans argument | commande pacman sans `sddm` ; aucun fichier écrit dans le dossier de conf de test |
| `install-arch-deps.sh sddm` | pacman reçoit `sddm` ; `10-dotfiles.conf` contient `[Theme]` `Current=fdt2k-dark` et `[X11]` `DisplayCommand=$HOME/.config/qtile/bin/screenlayout.d/sddm` (chemin développé) |
| Dossier de thèmes de test avec un vrai dossier `fdt2k-dark` | renommé en `fdt2k-dark.bak-*`, lien `fdt2k-dark` → `$HOME/.local/share/sddm/themes/fdt2k-dark` |
| Relance, lien déjà en place | aucun nouveau `.bak-*`, lien inchangé |
| Faux `sudo -u sddm test` en échec, `HOME` de test en 700 | avertissement nommant `$HOME`, ligne `chmod o+x …`, aucun `chmod` lancé, code 0 |
| `git ls-files .local/share/sddm/themes/fdt2k-dark/theme.conf.user` après fix | vide ; `git check-ignore` le reconnaît ; le fichier existe toujours |
| Relance | fichier réécrit, contenu identique |
| `screenlayout.d/sddm` absent du `HOME` de test | avertissement `missing or not executable`, code 0, fichier écrit |
| Faux `systemctl is-enabled sddm` → `disabled` | ligne `enable it with: sudo systemctl enable sddm` ; aucun `systemctl enable` lancé |
| Aucun accès à `/usr/share/sddm` | vérifié : aucune commande ne le mentionne hors du message de rappel |
| `install-arch-deps.sh foo` | message listant `sddm`, code 2 |
| Fixe — `install-arch-deps.sh sddm`, puis redémarrage | écrans réglés avant le login, thème `fdt2k-dark` avec le fond du thème courant |
| Laptop — `install-arch-deps.sh sddm` | avertissement sur `~` en 700 ; après le `chmod` affiché et un redémarrage, thème `fdt2k-dark` au login |
