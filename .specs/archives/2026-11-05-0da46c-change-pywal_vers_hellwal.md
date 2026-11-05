# Remplacer pywal par hellwal dans la chaîne de thème

Status: implemented
Chantier: divers

## Situation initiale

La chaîne de thème repose sur pywal (`wal`). Une image choisie produit une palette de 16 couleurs, écrite dans `~/.cache/wal/` et lue par tous les composants du bureau.

**Commandes pywal appelées**

| Fichier | Appel | Rôle |
|---|---|---|
| `.config/qtile/bin/theme/pick` | `wal -i $FOLDER/$choice` | génère le thème depuis l'image choisie dans `~/Pictures/themes` |
| `.config/qtile/bin/theme/reload` | `wal --vte -R` | recharge le dernier thème et recolore les terminaux ouverts, puis relance dunst et le K70 |
| `.zshrc` (ligne 149) | `wal --vte -Rq` | recolore chaque nouveau terminal au démarrage de zsh |

`--vte` retire la séquence de bordure qui produit des artefacts dans les terminaux VTE. Terminator, le terminal utilisé, est un terminal VTE.

**Fichiers du cache lus par les consommateurs**

| Fichier | Consommateur | Ce qui est lu |
|---|---|---|
| `~/.cache/wal/colors.json` | `.config/qtile/qtile_config/themes.py` | clés `wallpaper`, `alpha`, `colors` (`color0`..`color15` dans l'ordre) ; indices 0, 1, 2, 6, 7, 8. **Le module plante à l'import si le fichier manque** |
| `~/.cache/wal/colors.sh` | `.config/qtile/bin/theme/colorize-dunst` | `$color0`, `$color2`, `$color3`, `$color7`, au format `#rrggbb` |
| `~/.cache/wal/colors` | `.config/qtile/bin/theme/sddm` (lignes 1, 3, 8), `.config/qtile/bin/theme/colorize-k70` (ligne 2) | une couleur `#rrggbb` par ligne, ligne N = `color{N-1}` |
| `~/.cache/wal/colors-rofi-dark.rasi` | `.config/rofi/config.rasi` (`@theme`), `.config/rofi/colors/pywal.rasi` (`@import`, lui-même importé par les launchers et powermenu `type-1`), `.config/qtile/widgets/colors.rasi` (`@theme`) | le thème rofi « dark » de pywal : variables `@background`, `@foreground`, `@selected-normal-background`, `@selected-active-background`, `@selected-urgent-background`, `@alternate-background`… |

**Fichiers écrits par les dotfiles eux-mêmes dans `~/.cache/wal/`** (`bin/theme/pick`) : `wallpaper.png`, `current-theme.jpg` (fond SDDM et lockscreen), `.theme-$STR.jpg`.

## Motivation

- **Contexte** : pywal n'est plus maintenu. L'humain a choisi hellwal (version étudiée : 1.0.9), proche dans l'esprit mais différent dans ses sorties.
- **Objectif** : générer le thème avec hellwal, en gardant tous les consommateurs actuels inchangés.
- **Bénéfice** : un outil maintenu ; un seul point de bascule (les templates) ; retour à pywal possible ; contrastes garantis grâce au mode confort de hellwal.

Ce qui distingue hellwal de pywal, d'après l'agent `hellwal@lovecraft` (fil réseau `92b192`, réponses tirées du code de hellwal 1.0.9, non exécuté) :

- hellwal **n'installe aucun template**. Il lit les fichiers du premier niveau de `~/.config/hellwal/templates/` (ou de `-f <dir>`). Sans template, il ne génère rien ;
- chaque fichier généré porte **le nom de son template**, dans `~/.cache/hellwal/` par défaut ou dans `-o <dir>` ;
- les valeurs `%%colorN.hex%%` sortent **sans `#`** : le template doit l'écrire lui-même (`#%%colorN.hex%%`) ;
- `%%wallpaper%%` est le chemin **tel que passé à `-i`**, sans `realpath` ;
- `wal -R` n'a pas d'équivalent. On recharge en relançant `hellwal -i <même image>` **avec les mêmes options** : la palette vient du cache (clé : image + options), rien n'est recalculé ;
- hellwal recolore lui-même les terminaux ouverts à chaque exécution, avec une séquence de bordure que `--vte` retirait chez pywal. `--skip-term-colors` désactive cette diffusion ;
- `--comfort-mode` garantit les contrastes contre le fond : 7.2:1 pour color7/15, 5.2:1 pour color1–6, 6.2:1 pour color9–14, 4.7:1 pour color8 ;
- la palette n'a pas de notion d'`alpha` : dans le `colors.json` d'exemple, c'est un littéral.

## Changements demandés

Décisions de l'humain : des fichiers compatibles pywal sous `~/.cache/wal`, les templates dans `.config/hellwal/templates/`, la recoloration des terminaux par `terminal.sh` seul, et `--comfort-mode` activé.

### Templates hellwal versionnés

**Avant** : aucun template ; pywal génère ses fichiers avec ses propres templates internes.
**Après** : un nouveau dossier `.config/hellwal/templates/` (miroir de `~/.config/hellwal/templates/`, le dossier lu par défaut par hellwal, donc sans `-f`) contient cinq templates. Chacun produit, octet pour octet dans sa forme, le fichier que pywal produisait :

| Template | Contenu |
|---|---|
| `colors.json` | même forme que le `colors.json` de pywal : `wallpaper` (`%%wallpaper%%`, échappé JSON), `alpha` (littéral `"100"`), `special` (`background`, `foreground`, `cursor`), `colors` (`color0`..`color15`, dans l'ordre, valeurs `#%%colorN.hex%%`) |
| `colors.sh` | `color0='#%%color0.hex%%'` … `color15='#…'`, plus `background`, `foreground`, `cursor` et `wallpaper` — sans les `export` FZF / LS_COLORS de l'exemple `variables.sh` de hellwal |
| `colors` | seize lignes `#%%color0.hex%%` … `#%%color15.hex%%`, rien d'autre : ligne N = `color{N-1}`. **Pas** la forme de l'exemple hellwal, qui commence par background/foreground/cursor/border |
| `colors-rofi-dark.rasi` | reproduction du template `colors-rofi-dark.rasi` de pywal, avec chaque couleur remplacée par `#%%colorN.hex%%` (ou `%%background.hex%%` / `%%foreground.hex%%`, avec le `#`). **Pas** l'exemple `rofi.rasi` de hellwal, qui est un thème complet différent |
| `terminal.sh` | les `printf` OSC 4 / 10 / 11 / 12 de l'exemple `terminal.sh` de hellwal, **sans la ligne de bordure** (OSC 708 / 7044) |

### Invocation unique de hellwal

**Avant** : `wal -i <image>` dans `pick`, `wal --vte -R` dans `reload`.
**Après** : un nouveau script `.config/qtile/bin/theme/hellwal-apply <image>` porte **la seule** ligne d'appel :

```bash
hellwal -i "$(realpath "$1")" -o "$HOME/.cache/wal" --comfort-mode --skip-term-colors -q
```

Il diffuse ensuite `~/.cache/wal/terminal.sh` à chaque terminal ouvert, c'est-à-dire chaque `/dev/pts/[0-9]*` accessible en écriture : `sh ~/.cache/wal/terminal.sh > "$pts"`, une erreur d'écriture sur un pts n'interrompant pas la boucle. Les options d'apparence (`--comfort-mode`) n'existent qu'à cet endroit : pick et reload passent forcément les mêmes, condition pour que le cache de palette serve au rechargement.

### `bin/theme/pick`

**Avant** : `wal -i $FOLDER/$choice`.
**Après** : `$DIR/hellwal-apply "$FOLDER/$choice"`. Le reste du script ne change pas : `wallpaper.png`, `current-theme.jpg`, `.theme-$STR.jpg`, le redémarrage de Qtile, puis `reload` et `sddm`.

### `bin/theme/reload`

**Avant** : `wal --vte -R`.
**Après** : le script lit le chemin `wallpaper` de `~/.cache/wal/colors.json` (avec `python3`, déjà requis par Qtile, pas `jq`), puis appelle `$DIR/hellwal-apply "$wallpaper"`. La suite ne change pas : `colorize-dunst`, `colorize-k70`, `notify-send`.

### `.zshrc`

**Avant** : `wal --vte -Rq` (ligne 149).
**Après** : `[ -f ~/.cache/wal/terminal.sh ] && sh ~/.cache/wal/terminal.sh`. Aucun appel à hellwal au démarrage d'un shell : sinon, chaque nouveau terminal réécrirait tous les fichiers.

### Documentation

**Avant** : `CLAUDE.md`, `.config/qtile/CLAUDE.md` et les commentaires de `.config/qtile/qtile_config/themes.py` et de `bin/theme/colorize-dunst` parlent de pywal / `wal`.
**Après** :
- les deux `CLAUDE.md` décrivent la chaîne hellwal : templates dans `.config/hellwal/templates/`, sortie dans `~/.cache/wal/`, point d'appel unique `bin/theme/hellwal-apply`, et le premier lancement manuel nécessaire (voir Edge cases) ;
- la liste des dépendances de `.config/qtile/CLAUDE.md` remplace `pywal` par `hellwal` ;
- les commentaires de code sont mis à jour, sans changer le code.

## Règles métier impactées

Aucune : le dépôt n'a pas de `.specs/docs/business_rules/`, et une configuration de bureau personnelle n'a pas de règle métier.

## Fichiers concernés

| Fichier | Modification |
|---------|-------------|
| `.config/hellwal/templates/colors.json` | nouveau — template compatible pywal |
| `.config/hellwal/templates/colors.sh` | nouveau — template compatible pywal |
| `.config/hellwal/templates/colors` | nouveau — seize lignes `#rrggbb` |
| `.config/hellwal/templates/colors-rofi-dark.rasi` | nouveau — reproduction du template rofi dark de pywal |
| `.config/hellwal/templates/terminal.sh` | nouveau — OSC 4/10/11/12, sans bordure |
| `.config/qtile/bin/theme/hellwal-apply` | nouveau, exécutable — appel unique de hellwal + diffusion aux pts |
| `.config/qtile/bin/theme/pick` | `wal -i` → `hellwal-apply` |
| `.config/qtile/bin/theme/reload` | `wal --vte -R` → lecture de `wallpaper` + `hellwal-apply` |
| `.zshrc` | `wal --vte -Rq` → `sh ~/.cache/wal/terminal.sh` conditionnel |
| `CLAUDE.md` | chaîne de thème hellwal |
| `.config/qtile/CLAUDE.md` | section Color/Theme System et dépendances |
| `.config/qtile/qtile_config/themes.py` | commentaires seulement |
| `.config/qtile/bin/theme/colorize-dunst` | commentaire d'en-tête seulement |

## Migrations schéma

Aucune

## Migrations données

Aucune

## Contraintes à respecter

- Ne modifier **aucun consommateur** du cache : `themes.py` (hors commentaires), `colorize-dunst` (hors commentaire), `colorize-k70`, `sddm`, les `.rasi` de `.config/rofi/` et `.config/qtile/widgets/colors.rasi` continuent de lire les mêmes chemins, aux mêmes formats.
- Garder le dossier de sortie `~/.cache/wal/` et ne pas toucher aux fichiers que `pick` y écrit lui-même (`wallpaper.png`, `current-theme.jpg`, `.theme-*.jpg`).
- Aucune option d'apparence de hellwal ailleurs que dans `hellwal-apply`.
- Ne jamais lancer `hellwal --clear-cache` dans les scripts.
- Ne pas désinstaller pywal ni toucher au système : c'est un geste de l'humain sur son poste.
- Chemins `/home/fabien/...` existants laissés tels quels (règle du `CLAUDE.md`).
- Les commits suivent `## Commits` du `CLAUDE.md` ; jamais `config` / `configsave`.

## Edge cases

| Situation | Comportement attendu |
|-----------|---------------------|
| Premier passage : `~/.cache/wal/` ne contient encore aucun fichier produit par hellwal | Hors du code : la doc (`CLAUDE.md`) dit de lancer `bin/theme/hellwal-apply <image>` une fois avant de redémarrer Qtile, car `themes.py` plante si `colors.json` manque. Les fichiers pywal existants restent valides jusque-là |
| `pick` reçoit un chemin relatif ou contenant des espaces | `hellwal-apply` le passe par `realpath`, entre guillemets : `wallpaper` est toujours absolu |
| `reload` lancé alors que `colors.json` est absent ou que l'image de `wallpaper` n'existe plus | `reload` s'arrête avec un message sur stderr et un code non nul, **sans** appeler hellwal ni relancer dunst ou le K70 |
| Un pts n'est pas accessible en écriture (terminal d'un autre utilisateur, pts fermé pendant la boucle) | ignoré en silence, la boucle continue |
| Nouveau shell alors que `~/.cache/wal/terminal.sh` n'existe pas encore | rien ne s'exécute, aucun message : le shell démarre normalement |
| Couleurs de `--comfort-mode` différentes de celles de pywal pour la même image | attendu ; aucun réglage de compatibilité |
| `--light` (thème clair) | hors périmètre : non géré |

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`). Il n'y a pas de fichier de test à écrire. Les vérifications se font par commande, dans la session quand c'est possible, sinon à la main par l'humain sur son poste (hellwal et l'affichage ne sont pas dans le container).

| Cas | Attendu |
|-----|---------|
| `bash -n` sur `hellwal-apply`, `pick`, `reload` ; `zsh -n .zshrc` | aucune erreur de syntaxe |
| `grep -rn "wal -\|wal --" .zshrc .config/qtile/bin` | aucun appel à pywal restant |
| `grep -rn "hellwal " .config/qtile/bin .zshrc` | un seul appel à `hellwal`, dans `hellwal-apply` |
| Template `colors` | exactement 16 lignes, chacune `#%%colorN.hex%%`, N de 0 à 15 dans l'ordre |
| Template `colors.json` rendu avec des valeurs fictives (substitution `sed` des `%%…%%`) | JSON valide (`python3 -m json.tool`), clés `wallpaper`, `alpha`, `colors.color0`..`color15` présentes, valeurs `#rrggbb` |
| Template `colors.sh` rendu de même | sourçable par `bash`, `$color0`..`$color15` au format `#rrggbb` |
| Template `colors-rofi-dark.rasi` | définit chaque variable que les `.rasi` de `.config/rofi/` et `.config/qtile/widgets/` utilisent sans la définir eux-mêmes (`background`, `foreground`, `selected-normal-background`, `selected-active-background`, `selected-urgent-background`, `alternate-background`…) |
| Template `terminal.sh` | aucune séquence OSC 708 ni 7044 |
| Poste — `hellwal-apply ~/Pictures/themes/<image>` | `~/.cache/wal/{colors.json,colors.sh,colors,colors-rofi-dark.rasi,terminal.sh}` régénérés ; terminaux Terminator ouverts recolorés sans artefact de bordure |
| Poste — redémarrage Qtile, rofi, dunst (`reload`) | barre, launcher, powermenu et notifications aux nouvelles couleurs |
| Poste — `reload` sans changer d'image | même palette qu'après `pick` (cache de hellwal), terminaux recolorés |
| Poste — `reload` avec `colors.json` absent | message d'erreur, code non nul, dunst non relancé |
| Poste — nouveau terminal | couleurs appliquées par `terminal.sh` ; sans `terminal.sh`, démarrage normal sans message |
