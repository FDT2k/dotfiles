# Installeur de release GitHub : ActivityWatch dans le script d'installation

Status: draft
Chantier: divers

## Situation initiale

`.config/qtile/autostart.sh` tue puis relance ActivityWatch à chaque démarrage de session :

```bash
killall -9 aw-qt
killall -9 aw-server
killall -9 aw-watcher-afk
killall -9 aw-watcher-window
…
aw-qt &
```

`aw-qt` est appelé par son nom. Qtile n'a pas `~/bin` dans son `PATH` (seul `.zshrc` l'ajoute), comme on l'a vu pour hellwal.

ActivityWatch n'est pas dans les dépôts officiels d'Arch, et l'humain n'utilise plus l'AUR. Le projet publie à chaque version, sur `https://github.com/ActivityWatch/activitywatch/releases`, une archive Linux prête à l'emploi, `activitywatch-v<version>-linux-x86_64.zip`. Elle contient `aw-qt`, `aw-server` et les watchers.

`.config/qtile/bin/install-arch-deps.sh` installe des groupes de paquets officiels (`sudo pacman -S --needed`) et compile les outils non packagés avec `git_install` (clone dans `~/.local/src/<nom>`, `make`, copie dans `~/bin/<nom>`).

## Besoin

- **Qui** : l'humain, sur le laptop aujourd'hui et sur toute nouvelle machine.
- **Quoi** :
  - installer et mettre à jour ActivityWatch depuis l'archive officielle des releases GitHub, sans AUR ;
  - que la session le lance quel que soit le `PATH` de Qtile.
- **Pourquoi** : `autostart.sh` lance `aw-qt`, absent du laptop.

## Spécification fonctionnelle

### Règles métier

Aucune business rule : le dépôt n'a pas de `.specs/docs/business_rules/`.

Décision de l'humain : l'archive officielle des releases GitHub (option 1).

Règles :
1. **Fonction `release_install <nom> <dépôt github> <motif d'archive> <binaire>`** dans `install-arch-deps.sh` :
   - lit la dernière release par `curl -fsSL https://api.github.com/repos/<dépôt>/releases/latest` ;
   - en extrait (avec `python3`) le tag et l'URL du premier asset dont le nom correspond au motif (expression régulière) ;
   - si `~/.local/opt/<nom>/.version` contient déjà ce tag, il s'arrête là : `==> <nom> up to date (<tag>)` ;
   - sinon, il télécharge l'archive dans un dossier temporaire (`mktemp -d`) et la décompresse (`unzip -q`).
   - Il remplace ensuite `~/.local/opt/<nom>` : l'ancien dossier est renommé en `<nom>.old`, le nouveau est mis en place, puis `<nom>.old` est supprimé. Il écrit le tag dans `.version`.
   - Il crée le lien `~/bin/<binaire>` vers le binaire `<binaire>` trouvé dans l'archive, par `find … -name <binaire> -type f -perm -u+x`, à deux niveaux de profondeur au plus. Le chemin à l'intérieur de l'archive n'est donc pas supposé.
   - Messages : `==> release: <nom> <tag> (<dépôt>) → ~/.local/opt/<nom>`, puis `==> <nom> installed: ~/bin/<binaire>`.
2. Chaque étape en échec (API injoignable, aucun asset ne correspond au motif, téléchargement, décompression, binaire introuvable) arrête le script avec un code non nul et un message qui nomme l'étape. **L'installation existante n'est pas touchée** tant que la nouvelle n'est pas complète.
3. **Recette** en tête du script, à côté de `HELLWAL_GIT` :
   `ACTIVITYWATCH_RELEASE=(activitywatch ActivityWatch/activitywatch 'activitywatch-v[0-9.]+-linux-x86_64\.zip' aw-qt)`.
4. **Nouveau groupe `activitywatch`**, inclus dans les groupes par défaut : paquets `curl`, `unzip` et `python` (pour lire la réponse de l'API), puis `release_install` avec la recette ci-dessus.
5. **`autostart.sh`** lance ActivityWatch par un chemin résolu : `~/bin/aw-qt` s'il est exécutable, sinon `aw-qt` trouvé dans le `PATH`. S'il ne trouve rien, il ne lance rien, sans erreur. Les `killall` ne changent pas.

### Parcours utilisateur

1. L'humain lance `~/.config/qtile/bin/install-arch-deps.sh` (ou `… activitywatch`).
2. Le script télécharge la dernière release, l'installe dans `~/.local/opt/activitywatch` et crée `~/bin/aw-qt`.
3. Au prochain démarrage de session, `autostart.sh` lance `~/bin/aw-qt`.
4. Une relance du script ne retélécharge rien tant qu'aucune nouvelle version n'est publiée.

## Edge cases

| Situation | Comportement attendu |
|-----------|---------------------|
| Premier lancement | téléchargement, `~/.local/opt/activitywatch/` et `~/bin/aw-qt` créés |
| Relance, même version | `up to date (<tag>)`, rien de téléchargé |
| Nouvelle version publiée | remplacement de `~/.local/opt/activitywatch`, `.version` mis à jour, lien recréé |
| API injoignable ou limite de requêtes atteinte | arrêt, message nommant l'étape, installation existante intacte |
| Aucun asset ne correspond au motif | arrêt, message `no asset matching <motif> in <tag>`, installation existante intacte |
| `aw-qt` absent de l'archive | arrêt, `binary not found: aw-qt`, installation existante intacte |
| `~/bin` absent | créé |
| Session sans ActivityWatch installé | `autostart.sh` ne lance rien, sans erreur |
| Groupes lancés sans `activitywatch` | aucun appel à `curl` |

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

Aucun dans le dépôt : `~/.local/opt/activitywatch/` et `~/bin/aw-qt` sont créés sur la machine.

### Fichiers à modifier

| Fichier | Modification |
|---------|-------------|
| `.config/qtile/bin/install-arch-deps.sh` | fonction `release_install`, recette `ACTIVITYWATCH_RELEASE`, tableau `ACTIVITYWATCH_PKGS=(curl unzip python)`, groupe `activitywatch` (par défaut), en-tête et message de groupe inconnu |
| `.config/qtile/autostart.sh` | lancement de `aw-qt` par chemin résolu (`~/bin/aw-qt`, sinon `PATH`, sinon rien) |
| `.config/qtile/CLAUDE.md` | groupe `activitywatch` et `release_install` dans la ligne du script |

## Contraintes à respecter

- Dépôts officiels seulement pour pacman ; aucun AUR.
- Pas de `sudo` pour `release_install` : tout se passe dans le `HOME`.
- Ne jamais supprimer `~/.local/opt/<nom>` tant que la nouvelle version n'est pas prête.
- Aucun jeton GitHub : appel anonyme à l'API.
- `git_install` et les autres groupes ne changent pas.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`), et le container n'a pas accès à GitHub. Les cas se jouent avec un `HOME` de test et de faux `sudo` et `curl`. Le faux `curl` renvoie une réponse d'API fictive et une archive zip construite pour le test (avec `python3 -m zipfile`), contenant `activitywatch/aw-qt` exécutable.

| Cas | Attendu |
|-----|---------|
| `bash -n install-arch-deps.sh`, `bash -n autostart.sh` | aucune erreur |
| `install-arch-deps.sh activitywatch`, premier lancement | pacman reçoit `curl unzip python` ; `~/.local/opt/activitywatch/.version` = tag fictif ; `~/bin/aw-qt` → binaire de l'archive |
| Relance, même tag | `up to date`, un seul appel à `curl` (l'API) |
| Nouveau tag | archive retéléchargée, `.version` mis à jour, pas de `activitywatch.old` restant |
| Faux `curl` en échec sur l'API | code non nul, installation précédente intacte |
| Réponse d'API sans asset correspondant | code non nul, `no asset matching`, installation intacte |
| Archive sans `aw-qt` | code non nul, `binary not found`, installation intacte |
| `install-arch-deps.sh rofi` | aucun appel à `curl` |
| `install-arch-deps.sh` sans argument | groupe `activitywatch` inclus |
| `autostart.sh` : extrait de résolution joué avec `~/bin/aw-qt` présent / absent | lance `~/bin/aw-qt` / ne lance rien |
| Laptop — `install-arch-deps.sh activitywatch`, puis redémarrage de session | ActivityWatch tourne (icône dans la barre système, `aw-qt` dans `pgrep`) |
