# Thème de dunst généré par hellwal

Status: implemented
Chantier: divers

## Situation initiale

Les notifications passent par dunst (`notify-send` depuis les scripts de volume, `keybindings.py`, `bin/theme/pick`…). Le thème de dunst a été commencé mais jamais terminé.

`.config/qtile/bin/theme/colorize-dunst` est lancé par `bin/theme/reload`, donc à chaque changement de thème et au démarrage par `autostart.sh`. Il :
- source `~/.cache/wal/colors.sh` ;
- affiche `color3`, `color0` et `prout` sur sa sortie (restes de mise au point) ;
- fait `pkill dunst` puis relance `dunst` avec des options de couleur en ligne de commande (`-frame_width`, `-lfr`, `-nfr`, `-cfr`, `-lb`, `-nb`, `-cb`, `-lf`, `-bf`, `-cf`, `-nf`).

Ces options de couleur et de cadre en ligne de commande viennent d'anciennes versions de dunst. Les versions actuelles ne règlent ces valeurs que par fichier de configuration. Les couleurs du thème n'arrivent donc jamais à dunst.

Couleurs voulues par l'humain dans ce script :

| Urgence | Fond | Texte | Cadre |
|---|---|---|---|
| low | `color0` | `color2` | `color3` |
| normal | `color0` | `color7` | `color3` |
| critical | `color0` | `color2` | `color3` |

La chaîne de thème génère ses fichiers avec les templates hellwal de `.config/hellwal/templates/`, écrits dans `~/.cache/wal/` par `bin/theme/hellwal-apply` (`--comfort-mode` : contraste garanti contre `color0`).

**Prérequis** : l'humain versionne son `dunstrc` du poste fixe dans `.config/dunst/dunstrc` **avant l'implémentation**. Il porte ses réglages (police, géométrie, position…).

## Besoin

- **Qui** : l'humain, sur le poste fixe et le laptop.
- **Quoi** : des notifications dunst aux couleurs du thème courant, mises à jour à chaque changement de thème, avec ses propres réglages de dunst.
- **Pourquoi** : terminer le thème de dunst, aujourd'hui sans effet, et repérer d'un coup d'œil les notifications critiques (l'échec de `hellwal-apply`, par exemple).

## Spécification fonctionnelle

### Règles métier

Aucune business rule : le dépôt n'a pas de `.specs/docs/business_rules/`.

Règles :
1. `.config/dunst/dunstrc`, versionné par l'humain, reste **la seule source des réglages** de dunst. Seules ses couleurs sont surchargées.
2. Les couleurs viennent d'un **fichier de surcharge** (drop-in) que dunst lit après `dunstrc` : `~/.config/dunst/dunstrc.d/50-hellwal.conf`.
   - C'est un **lien symbolique versionné, relatif**, vers `../../../.cache/wal/dunst-colors.conf`.
   - Le fichier pointé est généré par le template hellwal `.config/hellwal/templates/dunst-colors.conf`.
3. Le template écrit les sections `[urgency_low]`, `[urgency_normal]` et `[urgency_critical]`, avec `background`, `foreground` et `frame_color` en `"#%%colorN.hex%%"`. Les couleurs reprennent la table ci-dessus, sauf le **cadre critique, qui passe en `color1`** (décision de l'humain).
4. `colorize-dunst` relance dunst sans option de couleur : `pkill dunst` puis `dunst &`. dunst relit alors `dunstrc` et la surcharge. Les `echo` de mise au point disparaissent.
5. Si `~/.cache/wal/dunst-colors.conf` n'existe pas encore (avant le premier `hellwal-apply`), le lien est cassé : dunst démarre avec le seul `dunstrc`, sans erreur bloquante.
6. Une notification qui arrive alors que dunst ne tourne pas le fait démarrer par D-Bus, et il lit aussi la surcharge : les couleurs sont donc là même sans passer par `colorize-dunst`.

### Parcours utilisateur

1. L'humain choisit un thème (`pick`).
2. `hellwal-apply` régénère `~/.cache/wal/dunst-colors.conf` avec les autres fichiers.
3. `reload` lance `colorize-dunst`, qui redémarre dunst.
4. La notification « theme reloaded » s'affiche aux nouvelles couleurs. Une notification critique a un cadre `color1`.

## Edge cases

| Situation | Comportement attendu |
|-----------|---------------------|
| `.config/dunst/dunstrc` absent au moment de l'implémentation | `kda-work` s'arrête avant toute modification et le signale : prérequis non rempli |
| `dunstrc` de l'humain qui définit déjà des couleurs dans `[urgency_*]` | laissé tel quel ; la surcharge l'emporte, car dunst la lit après |
| `~/.cache/wal/dunst-colors.conf` absent | lien cassé ignoré par dunst, qui démarre avec ses réglages seuls |
| dunst trop ancien pour lire `dunstrc.d/` (avant 1.9) | hors périmètre : couleurs non appliquées, réglages conservés ; à signaler si constaté |
| `colorize-dunst` lancé sans `colors.sh` | il ne source plus `colors.sh` : aucun effet |

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
| `.config/hellwal/templates/dunst-colors.conf` | template hellwal des couleurs par urgence |
| `.config/dunst/dunstrc.d/50-hellwal.conf` | lien symbolique relatif vers `../../../.cache/wal/dunst-colors.conf` |

### Fichiers à modifier

| Fichier | Modification |
|---------|-------------|
| `.config/qtile/bin/theme/colorize-dunst` | ne source plus `colors.sh`, plus d'options de couleur ni d'`echo` : `pkill dunst` puis `dunst &` ; commentaire d'en-tête à jour |
| `CLAUDE.md` | bullet Thème : dunst, avec `dunstrc` versionné et couleurs par la surcharge `dunstrc.d/50-hellwal.conf` |
| `.config/qtile/CLAUDE.md` | section Color/Theme System : même information ; `colorize-dunst` redémarre dunst |

## Contraintes à respecter

- Ne pas modifier le contenu de `.config/dunst/dunstrc` versionné par l'humain.
- Les couleurs ne vivent que dans le template ; aucune couleur en dur dans `colorize-dunst`.
- `hellwal-apply`, `pick`, `reload` et les autres templates ne changent pas.
- Pas de paquet nouveau : `dunst` et `libnotify` sont déjà dans le groupe `dunst` de `install-arch-deps.sh`.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`), et dunst n'est pas installé dans le container. Les cas se jouent par commande, avec un rendu fictif du template et un faux `dunst`/`pkill`, puis à l'œil sur le laptop.

| Cas | Attendu |
|-----|---------|
| `bash -n .config/qtile/bin/theme/colorize-dunst` | aucune erreur |
| Reproduit le bug — avant fix, `colorize-dunst` | lance `dunst` avec des options `-lb`, `-nf`… et affiche `prout` |
| Après fix, `colorize-dunst` avec faux `pkill`/`dunst` | `pkill dunst` puis `dunst` sans argument ; rien sur la sortie |
| Template rendu avec des valeurs fictives | trois sections `[urgency_low]`, `[urgency_normal]`, `[urgency_critical]`, chacune avec `background`, `foreground`, `frame_color` au format `"#rrggbb"` ; cadre critique = `color1`, autres cadres = `color3` |
| `readlink .config/dunst/dunstrc.d/50-hellwal.conf` | `../../../.cache/wal/dunst-colors.conf` ; résolu depuis un `HOME` de test, il pointe vers `$HOME/.cache/wal/dunst-colors.conf` |
| `git ls-files -s .config/dunst/dunstrc.d/50-hellwal.conf` | mode `120000` (lien symbolique versionné) |
| Laptop — `dunst --version` | 1.9 ou plus récent (lecture de `dunstrc.d/`) |
| Laptop — changement de thème | « theme reloaded » aux couleurs du thème ; `notify-send -u critical test` a un cadre `color1` |
