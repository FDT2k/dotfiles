# Remplacer Barrier par Deskflow : clavier et souris du fixe partagés avec le laptop

Status: draft
Chantier: divers

## Situation initiale

Le menu « Barrier » (`Key([mod, alt], "b", lazy.spawn(command.barrier))`, `command.barrier` = `bin/run.sh barrier.d Barrier`) propose deux entrées dans `.config/qtile/bin/barrier.d/`, écrites pour des machines qui n'existent plus :
- `laptop-alien-up` lance le serveur `barriers -c ~/.config/qtile/.conf/barrier.sgc --restart` (fichier non versionné), puis, en ssh vers `fabien@fdtacer.lan`, le client `barrierc --name FDTACER 192.168.64.108:24800` sur `DISPLAY=:1.0` ;
- `laptop-alien-down` tue le client distant (ssh) et le serveur local.

Barrier n'est plus maintenu. Ses successeurs sont dans les dépôts officiels d'Arch (`extra`) : `deskflow 1.27.0` et `input-leap 3.0.3`.

Machines actuelles : le fixe **daoloth** et le laptop **abhoth**. Les dispositions d'écran et SDDM se règlent déjà par hostname (`uname -n`, `bin/screenlayout`).

## Motivation

- **Contexte** : à la maison, l'humain pose le laptop **sous** les écrans du fixe et veut piloter les deux avec le clavier et la souris du fixe.
- **Objectif** : remplacer Barrier par **Deskflow**, sans ssh entre les machines et sans adresse IP en dur.
- **Bénéfice** : un outil maintenu, une config versionnée et la même mécanique sur les deux machines (rôle déduit du hostname).

## Changements demandés

Décisions de l'humain : **Deskflow** ; **fixe serveur, laptop client** ; le laptop est **en dessous** des écrans du fixe ; démarrage par un **menu on/off**.

> **Prérequis avant implémentation** : la ligne de commande de Deskflow 1.27 (noms des binaires, options du serveur et du client, chiffrement TLS) n'est pas connue avec certitude dans la session de rédaction. L'humain installe `deskflow` sur le laptop et colle, dans la conversation ou dans une note de cette spec, la sortie de `pacman -Ql deskflow | grep /usr/bin/` et l'aide du ou des binaires serveur et client (`--help`). `kda-work` s'arrête si ces informations manquent, et ne devine aucune option.

### Configuration du serveur

**Avant** : `~/.config/qtile/.conf/barrier.sgc`, non versionné.
**Après** : `.config/deskflow/deskflow-server.conf`, versionné, au format texte hérité de Synergy et Barrier (sections `screens` et `links`) :

```
section: screens
	daoloth:
	abhoth:
end

section: links
	daoloth:
		down = abhoth
	abhoth:
		up = daoloth
end
```

Les noms d'écran sont les hostnames. La souris passe au laptop par le bas des écrans du fixe, et revient par le haut de l'écran du laptop.

### Menu

**Avant** : `bin/barrier.d/` (`laptop-alien-up`, `laptop-alien-down`), ssh vers une autre machine, IP en dur.
**Après** : `bin/deskflow.d/` avec deux entrées, `on` et `off`. Elles déduisent leur rôle de `uname -n` :
- **daoloth**, `on` : arrête un serveur ou un client Deskflow déjà lancé, puis démarre le **serveur** en arrière-plan avec `~/.config/deskflow/deskflow-server.conf`, sous le nom `daoloth`.
- **abhoth**, `on` : arrête un serveur ou un client Deskflow déjà lancé, puis démarre le **client** sous le nom `abhoth`, vers `daoloth.lan`. L'adresse du serveur est une variable en tête du script (`DESKFLOW_SERVER=daoloth.lan`), comme l'ancien `fdtacer.lan`.
- **`off`**, sur les deux : arrête le serveur ou le client Deskflow de la machine.
- **Autre machine** : `on` affiche une notification « Deskflow : pas de rôle pour `<hostname>` » et ne lance rien.
- Chaque `on` et chaque `off` affiche une notification (`notify-send`) qui dit ce qui a été lancé ou arrêté.
- Les commandes exactes (binaires, options, chiffrement) suivent les informations du prérequis.

Le raccourci reste `mod+alt+b`. `command.barrier` est renommé `command.deskflow` et pointe vers `bin/run.sh deskflow.d Deskflow`.

### Installation

**Avant** : Barrier n'est installé par aucun groupe.
**Après** : nouveau groupe **`deskflow`** dans `install-arch-deps.sh`, inclus dans les groupes par défaut, avec le paquet `deskflow`.

### Nettoyage

`bin/barrier.d/` est supprimé.

## Règles métier impactées

Aucune : le dépôt n'a pas de `.specs/docs/business_rules/`.

## Fichiers concernés

| Fichier | Modification |
|---------|-------------|
| `.config/deskflow/deskflow-server.conf` | nouveau — écrans `daoloth`, `abhoth`, laptop en dessous |
| `.config/qtile/bin/deskflow.d/on` | nouveau — serveur sur daoloth, client sur abhoth, notification |
| `.config/qtile/bin/deskflow.d/off` | nouveau — arrêt, notification |
| `.config/qtile/bin/barrier.d/` | supprimé |
| `.config/qtile/qtile_config/commands.py` | `barrier` → `deskflow`, `bin/run.sh deskflow.d Deskflow` |
| `.config/qtile/qtile_config/keybindings.py` | `mod+alt+b` → `command.deskflow` |
| `.config/qtile/bin/install-arch-deps.sh` | groupe `deskflow` (par défaut) |
| `.config/qtile/CLAUDE.md` | menu `deskflow.d` à la place de `barrier.d`, groupe `deskflow` |
| `CLAUDE.md` | une ligne : partage clavier/souris par Deskflow, rôle par hostname, config `.config/deskflow/` |

## Migrations schéma

Aucune

## Migrations données

Aucune

## Contraintes à respecter

- Aucun ssh d'une machine vers l'autre ; aucune adresse IP en dur.
- Pas de démarrage automatique : seulement le menu.
- Ne deviner aucune option de Deskflow : uniquement celles du prérequis.
- Ne pas toucher à `bin/run.sh` ni aux autres menus `.d`.
- Dépôts officiels seulement.

## Edge cases

| Situation | Comportement attendu |
|-----------|---------------------|
| `on` alors que Deskflow tourne déjà | l'ancien processus est arrêté, puis relancé : jamais deux instances |
| `off` alors que rien ne tourne | notification « Deskflow : déjà arrêté », code 0 |
| Laptop `on` alors que le fixe n'est pas joignable | le client est lancé et se reconnecte quand le serveur apparaît (comportement normal de Deskflow) ; notification de lancement |
| Hostname autre que daoloth ou abhoth | `on` : notification « pas de rôle », rien de lancé |
| `deskflow-server.conf` absent (dotfiles non à jour) sur le fixe | `on` : notification d'erreur, rien de lancé |
| Première connexion avec chiffrement TLS (empreinte à accepter) | traité selon l'aide de Deskflow collée au prérequis ; à défaut, documenté dans `CLAUDE.md` comme geste unique à faire dans l'interface graphique |

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`), et Deskflow n'est pas installé dans le container. Les cas se jouent avec de faux `uname`, `notify-send`, `pkill` et binaires Deskflow, puis sur les deux machines.

| Cas | Attendu |
|-----|---------|
| `sh -n` / `bash -n` sur `deskflow.d/on` et `deskflow.d/off`, `py_compile` des modules Qtile | aucune erreur |
| Faux `uname -n` = `daoloth`, `on` | arrêt préalable, puis binaire serveur lancé avec la config `~/.config/deskflow/deskflow-server.conf` et le nom `daoloth` ; notification |
| Faux `uname -n` = `abhoth`, `on` | arrêt préalable, puis binaire client lancé vers `daoloth.lan` avec le nom `abhoth` ; notification |
| Faux `uname -n` = `inconnu`, `on` | notification « pas de rôle », aucun binaire lancé |
| `off` | arrêt du serveur ou du client ; notification |
| `deskflow-server.conf` | sections `screens` (daoloth, abhoth) et `links` (`down = abhoth`, `up = daoloth`) |
| `grep -rn barrier .config/qtile` | aucun résultat |
| `install-arch-deps.sh deskflow` (faux `sudo`) / sans argument | pacman reçoit `deskflow` / `deskflow` inclus |
| Maison — fixe `on`, laptop `on` | la souris du fixe passe au laptop par le bas de ses écrans, le clavier suit ; `off` sur les deux arrête le partage |
