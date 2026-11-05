# Installeur git dans le script d'installation : hellwal depuis le fork FDT2k

Status: implemented
Chantier: divers

## Situation initiale

`.config/qtile/bin/install-arch-deps.sh` installe des groupes de paquets (`rofi`, `theme`, `lock`, `dunst`, `terminator`) par `sudo pacman -S --needed`. Il ne passe que par les dépôts officiels : l'humain n'utilise plus l'AUR.

hellwal n'est pas dans les dépôts officiels. Pour le groupe `theme`, le script cherche aujourd'hui un binaire hellwal aux emplacements de `bin/theme/hellwal-apply` (`PATH`, `~/.config/qtile/bin/hellwal`, `~/bin/hellwal`, `~/.local/bin/hellwal`) :
- trouvé → `hellwal present: …` ;
- absent → message « drop the binary in … », sortie en code 1.

Le binaire est donc posé à la main, sans source ni moyen de le mettre à jour.

`hellwal-apply` cherche hellwal dans cet ordre : `PATH`, `~/.config/qtile/bin/hellwal`, `~/bin/hellwal`, `~/.local/bin/hellwal`. Qtile ne lit pas `.zshrc`, qui seul ajoute `~/bin` au `PATH`.

## Besoin

- **Qui** : l'humain, en installant une machine (le laptop aujourd'hui).
- **Quoi** : un **installeur git** réutilisable dans `install-arch-deps.sh`. Il clone un dépôt, compile avec `make` et copie le binaire dans `~/bin`. Premier cas : hellwal, depuis le fork de l'humain `https://github.com/FDT2k/hellwal.git`.
- **Pourquoi** : installer et mettre à jour hellwal sans AUR ni copie manuelle, et disposer du même mécanisme pour les prochains outils non packagés.

## Spécification fonctionnelle

### Règles métier

Aucune business rule : le dépôt n'a pas de `.specs/docs/business_rules/`.

Décisions de l'humain :
1. L'installeur est une **fonction de `install-arch-deps.sh`**, pas un script séparé.
2. Les sources sont clonées dans **`~/.local/src/<nom>`** et y restent.
3. À **chaque lancement**, le dépôt est mis à jour (`git pull`), recompilé et le binaire recopié, même si le binaire existe déjà.

Règles :
1. `git_install <nom> <url> <binaire>` :
   - `<binaire>` est le chemin du binaire produit, relatif à la racine du dépôt.
   - Clone `<url>` dans `~/.local/src/<nom>` s'il n'y est pas ; sinon `git -C ~/.local/src/<nom> pull --ff-only`.
   - Lance `make -C ~/.local/src/<nom>`.
   - Copie `~/.local/src/<nom>/<binaire>` vers `~/bin/<nom>` avec `install -m 755`, en créant `~/bin` s'il manque.
   - Affiche `==> git: <nom> (<url>) → ~/bin/<nom>`, puis `==> <nom> installed: ~/bin/<nom>`.
2. Toute étape en échec arrête le script avec un code non nul et un message qui nomme l'étape (`clone`, `pull`, `make`, `binary not found`). Le binaire déjà en place dans `~/bin` n'est pas touché tant que la copie n'a pas réussi.
3. Le groupe `theme` ajoute aux paquets pacman les outils de compilation `git`, `make` et `gcc`. Après pacman, il appelle `git_install hellwal https://github.com/FDT2k/hellwal.git hellwal`. La vérification actuelle « hellwal present / drop the binary » disparaît.
4. Après l'installation, le script **avertit** (sans rien supprimer) si un autre hellwal **masquerait** `~/bin/hellwal` pour `hellwal-apply` :
   - un `~/.config/qtile/bin/hellwal`, qui passe avant `~/bin` ;
   - ou un `hellwal` dans le `PATH` du script qui n'est pas `~/bin/hellwal`.

   Message : `==> warning: <chemin> shadows ~/bin/hellwal for hellwal-apply — remove it to use the fresh build`.
5. Les recettes git vivent en tête du script, à côté des tableaux de paquets, pour que la suivante s'ajoute en une ligne.

### Parcours utilisateur

1. L'humain lance `~/.config/qtile/bin/install-arch-deps.sh` (ou `… theme`).
2. Le script installe les paquets pacman, dont `git`, `make` et `gcc`.
3. Il clone `FDT2k/hellwal` dans `~/.local/src/hellwal` (ou fait un `pull` s'il y est), compile, copie `hellwal` dans `~/bin/hellwal`.
4. Si un ancien binaire masque le nouveau, il le signale.
5. `hellwal-apply` trouve `~/bin/hellwal` (repli après le `PATH` et `~/.config/qtile/bin`).

## Edge cases

| Situation | Comportement attendu |
|-----------|---------------------|
| Premier lancement, `~/.local/src/hellwal` absent | `git clone`, `make`, copie dans `~/bin/hellwal` |
| Relance, clone présent | `git pull --ff-only`, `make`, recopie, même si `~/bin/hellwal` existe |
| `~/.local/src/hellwal` existe mais n'est pas un dépôt git | arrêt, message `~/.local/src/hellwal exists and is not a git repository`, rien n'est supprimé |
| `git pull --ff-only` refuse (modifications locales, historique divergent) | arrêt, message nommant `pull` et le dossier, ancien binaire intact |
| Pas de réseau, ou URL injoignable | arrêt sur `clone` ou `pull`, ancien binaire intact |
| `make` échoue | arrêt, message nommant `make`, ancien binaire intact |
| `make` réussit mais `<binaire>` est absent | arrêt, `binary not found: ~/.local/src/hellwal/hellwal`, ancien binaire intact |
| `~/bin` absent | créé |
| `~/.config/qtile/bin/hellwal` présent (binaire posé à la main) | build installé dans `~/bin`, avertissement de masquage ; aucun fichier supprimé |
| Groupes lancés sans `theme` (`rofi lock`…) | aucun installeur git appelé, ni `git`/`make`/`gcc` installés |
| Dépendances de compilation de hellwal autres que `make`/`gcc` | hors périmètre : si la compilation les réclame, `make` échoue et le script s'arrête ; on ajoutera le paquet au groupe |

## Conception technique

### Migrations schéma

Aucune

### Migrations données

Aucune

### Actions / Listeners

Sans objet (script shell).

### Panel / UI (Filament)

Sans objet.

### Fichiers à créer

Aucun.

### Fichiers à modifier

| Fichier | Modification |
|---------|-------------|
| `.config/qtile/bin/install-arch-deps.sh` | fonction `git_install` ; recette hellwal en tête ; `git make gcc` dans `THEME_PKGS` ; remplacement de la vérification hellwal par `git_install` + avertissement de masquage ; en-tête et commentaires à jour |
| `.config/qtile/CLAUDE.md` | ligne du script : hellwal compilé depuis `FDT2k/hellwal` dans `~/.local/src/hellwal`, installé dans `~/bin`, recettes git en tête du script |
| `CLAUDE.md` | bullet Thème : le binaire hellwal vient de `install-arch-deps.sh` (fork `FDT2k/hellwal`, `~/bin/hellwal`) |

## Contraintes à respecter

- Dépôts officiels seulement pour pacman ; aucun gestionnaire AUR.
- Ne jamais supprimer un binaire existant ailleurs que dans `~/bin/<nom>`, ni un clone dans `~/.local/src/`.
- Pas de `sudo` pour l'installeur git : tout se passe dans le `HOME` de l'utilisateur.
- `hellwal-apply` et son ordre de recherche ne changent pas.
- Ne rien versionner du clone ni du binaire (`.config/qtile/.gitignore` couvre déjà `bin/hellwal`).
- Le comportement des groupes `rofi`, `lock`, `dunst`, `terminator` ne change pas.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`), et le container n'a ni réseau vers GitHub ni pacman. Les cas se jouent avec un `HOME` de test et de faux `sudo`, `git`, `make`. Le faux `git clone` crée un dépôt local avec un Makefile qui produit `hellwal`. La vérification réelle se fait sur le laptop.

| Cas | Attendu |
|-----|---------|
| `bash -n .config/qtile/bin/install-arch-deps.sh` | aucune erreur |
| `install-arch-deps.sh theme`, premier lancement | pacman reçoit `git make gcc` ; clone dans `$HOME/.local/src/hellwal` ; `make` lancé ; `$HOME/bin/hellwal` exécutable |
| Relance, clone présent | `pull --ff-only` (pas de clone) ; `make` ; binaire recopié (date modifiée) |
| Faux `make` en échec | code non nul, message `make`, `$HOME/bin/hellwal` précédent inchangé |
| Makefile qui ne produit pas `hellwal` | code non nul, `binary not found`, ancien binaire inchangé |
| `~/.local/src/hellwal` est un dossier ordinaire | code non nul, message « not a git repository », dossier intact |
| `$HOME/.config/qtile/bin/hellwal` présent | installation faite, avertissement `shadows ~/bin/hellwal` |
| `install-arch-deps.sh rofi lock` | ni `git`/`make`/`gcc` dans la commande pacman, aucun appel à `git` |
| Laptop — `install-arch-deps.sh theme` | `~/bin/hellwal` compilé depuis `FDT2k/hellwal` ; un changement de thème depuis Qtile fonctionne |
