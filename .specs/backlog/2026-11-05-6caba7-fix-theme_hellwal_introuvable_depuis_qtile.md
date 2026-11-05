# Changement de thème sans effet depuis Qtile : hellwal introuvable, échec silencieux

Status: draft
Chantier: divers

## Situation initiale

Le changement de thème passe par `.config/qtile/bin/theme/pick`. Qtile le lance par le raccourci `pick_theme` de `.config/qtile/qtile_config/keybindings.py` (`command.theme`, résolu en `../bin/theme/pick <workspace>` dans `commands.py`). Le script :

1. affiche les images de `~/Pictures/themes` dans rofi ;
2. copie l'image choisie (`wallpaper.png`, `current-theme.jpg`, lien `.theme-$STR.jpg` dans `~/.cache/wal/`) ;
3. appelle `bin/theme/hellwal-apply`, le seul point d'appel de hellwal, posé par la spec `0da46c` ([archive](../archives/2026-11-05-0da46c-change-pywal_vers_hellwal.md)) ;
4. redémarre Qtile, puis source `reload` et `sddm`.

`hellwal-apply` appelle `hellwal` par son nom : il compte sur le `PATH` de l'appelant. Sur le laptop, hellwal n'est pas un paquet système. C'est un binaire placé à la main dans `~/bin`, et l'humain prévoit de le mettre plutôt dans `~/.config/qtile/bin/`. `~/bin` n'entre dans le `PATH` que par `.zshrc` (`export PATH=$PATH:...:$HOME/bin`). Une session X lancée par le gestionnaire de connexion ne lit pas `.zshrc`, et `~/.config/qtile/bin/` n'est dans aucun `PATH`.

Aucun script de la chaîne ne vérifie les codes de retour, et `pick` est lancé par Qtile : sa sortie d'erreur n'est visible nulle part.

## Problème

- **Symptôme** : sur le laptop, choisir une image dans le menu des thèmes redémarre Qtile, mais le thème ne change pas. Le log de Qtile montre, après chaque redémarrage :
  ```
  WARNING libqtile themes.py:load_colors() theme: /home/fabien/.cache/wal/colors.json unusable ([Errno 2] No such file or directory …), using default palette
  ```
  Le même `hellwal-apply`, lancé à la main depuis zsh, réussit (`code=0`) et produit `colors.json`.
- **Déclencheur** : un hellwal installé hors des répertoires système (`~/bin`, `~/.config/qtile/bin/`), et `pick` lancé depuis Qtile (ou `reload` depuis `autostart.sh`), dont le `PATH` ne contient pas ce répertoire.
- **Impact** :
  - changement de thème et rechargement au démarrage (`autostart.sh` → `reload`) sans effet ;
  - Qtile redémarre pour rien, sur la palette par défaut ;
  - `current-theme.jpg` (fond SDDM et lockscreen) est quand même remplacé par la nouvelle image, alors que les couleurs restent les anciennes.

## Comportement attendu

1. `hellwal-apply` trouve hellwal quel que soit l'appelant (Qtile, rofi, autostart, terminal), dans cet ordre :
   1. le `PATH` de l'appelant ;
   2. `~/.config/qtile/bin/hellwal` (calculé depuis l'emplacement du script : `$(dirname "$0")/../hellwal`) ;
   3. `~/bin/hellwal` ;
   4. `~/.local/bin/hellwal`.
2. hellwal introuvable : `hellwal-apply` écrit `hellwal-apply: hellwal not found (PATH, <les trois chemins>)` sur stderr et sort en code 127, sans rien écrire.
3. `hellwal-apply` crée `~/.cache/wal/` s'il n'existe pas, avant d'appeler hellwal.
4. `pick` :
   - menu rofi annulé (choix vide) ou choix qui n'est pas un fichier de `~/Pictures/themes` → **arrêt silencieux**, code 0, rien de modifié, pas de redémarrage ;
   - appelle `hellwal-apply` **avant** de toucher aux fichiers de `~/.cache/wal/` ;
   - `hellwal-apply` en échec → **notification critique** (`notify-send -u critical "Thème" "hellwal-apply a échoué (code N)"`), code non nul, aucune copie, aucun redémarrage, ni `reload` ni `sddm` ;
   - succès → le reste du script se déroule comme aujourd'hui.

> Invariants : `hellwal-apply` reste le seul appel de hellwal, avec les mêmes options ; les consommateurs du cache ne changent pas.

## Comportement actuel (avant fix)

- `pick` depuis Qtile, hellwal dans `~/bin` ou `~/.config/qtile/bin/` → `hellwal: command not found` invisible, Qtile redémarré, `colors.json` absent, palette par défaut.
- `pick`, menu annulé → `$choice` vide : `cp -a ~/Pictures/themes/ ~/.cache/wal/current-theme.jpg` copie le **dossier**, `hellwal-apply` reçoit le dossier, Qtile redémarre.
- Laptop neuf sans `~/.cache/wal/` → le `convert` et le `cp` de `pick` échouent. Le comportement de hellwal avec un `-o` absent n'est pas vérifié : la création du dossier le couvre.

## Cause identifiée

- `.config/qtile/bin/theme/hellwal-apply` (ligne 12) — `hellwal` appelé par son nom, sans repli hors du `PATH` ; aucun `mkdir` de `~/.cache/wal`.
- `.config/qtile/bin/theme/pick` (lignes 12-31) — ni le choix rofi ni le code de retour de `hellwal-apply` ne sont vérifiés ; les copies dans `~/.cache/wal/` ont lieu avant l'appel de hellwal.

## Solution

### `bin/theme/hellwal-apply`

Avant l'appel de hellwal :
- `mkdir -p "$HOME/.cache/wal"` ;
- résoudre le binaire dans l'ordre du comportement attendu (1). Utiliser `command -v hellwal` pour le `PATH`, puis tester `-x` sur chaque chemin de repli. Garder le chemin trouvé dans une variable, et l'appeler par ce chemin avec les mêmes arguments qu'aujourd'hui ;
- introuvable → message sur stderr, `exit 127`.

La ligne d'appel et ses options (`-i "$(realpath "$1")" -o "$HOME/.cache/wal" --comfort-mode --skip-term-colors -q`) ne changent pas.

### `bin/theme/pick`

- Après le menu rofi : `[ -n "$choice" ] && [ -f "$FOLDER/$choice" ] || exit 0`.
- Déplacer l'appel `"$DIR/hellwal-apply" "$FOLDER/$choice"` juste après cette vérification, avant `convert`. En échec : `notify-send -u critical "Thème" "hellwal-apply a échoué (code $code)"`, puis `exit "$code"`.
- Le reste — `convert`, `cp`, liens, redémarrage, `reload`, `sddm` — reste dans le même ordre, inchangé.
- Variables de chemin guillemetées sur les lignes touchées (`"$FOLDER/$choice"`).

### Documentation

Dans `CLAUDE.md` (bullet Thème) et `.config/qtile/CLAUDE.md` (Color/Theme System) : `hellwal-apply` trouve hellwal dans le `PATH`, puis dans `~/.config/qtile/bin/`, `~/bin` et `~/.local/bin`.

## Contraintes à respecter

- **Le binaire hellwal n'est pas versionné** : `~/.config/qtile/bin/hellwal` reste un fichier local de chaque machine. Ajouter `bin/hellwal` à `.config/qtile/.gitignore`, pour qu'un `git add` du dossier ne l'embarque pas dans ce clone. Le bare de l'humain ne suit de toute façon pas les fichiers non ajoutés.
- Ne pas toucher au `PATH` global de la session : ni `.zshrc`, ni `.xprofile`, ni `autostart.sh`.
- `hellwal-apply` reste le seul appel de hellwal ; ses options ne changent pas.
- `reload` n'est pas modifié : il passe déjà par `hellwal-apply` et s'arrête déjà en erreur.
- Hors périmètre : l'option `-lines` de rofi dans `pick`, le `convert` d'ImageMagick, l'écriture de `sddm` dans `/usr/share`.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Les vérifications se font par commande dans la session, avec un faux hellwal et un `PATH` réduit, puis à la main sur le laptop.

| Cas | Attendu |
|-----|---------|
| `bash -n` sur `hellwal-apply` et `pick` | aucune erreur |
| Reproduit le bug — avant fix, `env PATH=/usr/bin:/bin hellwal-apply img.jpg` avec le faux hellwal dans `~/bin` (HOME de test) | `hellwal: command not found`, code non nul |
| Après fix, même commande, faux hellwal dans `$HOME/bin` | hellwal appelé par `$HOME/bin/hellwal`, code 0 |
| Après fix, faux hellwal dans `$HOME/.config/qtile/bin/` (script lancé depuis `$HOME/.config/qtile/bin/theme/`) | appelé par ce chemin, prioritaire sur `~/bin` |
| Après fix, faux hellwal dans le `PATH` | appelé par le `PATH`, prioritaire sur les replis |
| Après fix, aucun hellwal | message `hellwal not found` sur stderr, code 127, `~/.cache/wal` sans nouveau fichier |
| Après fix, HOME de test sans `~/.cache/wal` | dossier créé, puis hellwal appelé |
| `pick` avec un faux `rofi` qui renvoie une chaîne vide | code 0, aucun fichier créé dans `~/.cache/wal`, faux `qtile` jamais appelé |
| `pick` avec un faux `hellwal-apply` qui sort en code 3 | faux `notify-send` appelé avec `-u critical`, code 3, pas de `current-theme.jpg`, faux `qtile` jamais appelé |
| `pick` nominal (faux rofi, faux hellwal, faux qtile/notify-send) | `hellwal-apply` appelé avant `cp` ; `current-theme.jpg` copié ; `qtile cmd-obj -o cmd -f restart` appelé |
| Laptop — hellwal dans `~/.config/qtile/bin/`, changement de thème depuis Qtile | les couleurs changent après le redémarrage, plus d'avertissement `colors.json unusable` dans le log |
