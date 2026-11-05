# Plan d'implémentation — 2026-11-05

> Généré par kda-plan. Ne pas implémenter directement — utiliser `kda-work {hash}` pour chaque spec.

Filtre : `8d134c`, `861406`, `9cf61c`.

## Résumé

3 specs actives · 0 en cours · 3 en attente

Aucun chantier déclaré (pas de `.specs/chantiers.md`, pas de chantier actif) : les trois specs sont en `divers`.

## 1. Specs en cours (`in-progress`)

Aucune.

---

## 2. Specs à implémenter (`draft`)

> Ordre d'implémentation recommandé.

| # | Hash | Spec | Type | Domaine | Chantier | Dépend de |
|---|------|------|------|---------|----------|-----------|
| 1 | `8d134c` | Nettoyage des écrans : presets morts, anciennes machines, luminosité cassée | quality | qtile / écrans | divers | — |
| 2 | `861406` | Groupe sddm du script d'installation : disposition d'écrans et thème fdt2k-dark | feature | install / sddm | divers | — |
| 3 | `9cf61c` | Dispositions d'écran par machine : `{hostname}.sh`, variantes, menu rofi | feature | qtile / écrans | divers | `8d134c`, `861406` |

### Détail

#### 1. `8d134c` — Nettoyage des écrans : presets morts, anciennes machines, luminosité cassée

**Type** : quality
**Domaine** : qtile / écrans
**Chantier** : divers
**Objectif** : supprimer les scripts xrandr des machines disparues, `bin/monitor_layout/`, `brightness.sh`, les fonctions et raccourcis morts (`mod+q`, `mod+alt+1/2/3`) pour ne garder que `daoloth.sh`, `sddm` et `arandr` dans le menu.
**Dépendances** : aucune (cite `861406` seulement pour justifier la conservation du lien `sddm`)
**Fichier** : `.specs/backlog/2026-11-05-8d134c-quality-nettoyage_ecrans.md`

#### 2. `861406` — Groupe sddm du script d'installation

**Type** : feature
**Domaine** : install / sddm
**Chantier** : divers
**Objectif** : ajouter à `install-arch-deps.sh` un groupe `sddm` (hors défaut) qui installe SDDM, écrit `/etc/sddm.conf.d/10-dotfiles.conf` (`DisplayCommand` → `screenlayout.d/sddm`, thème `fdt2k-dark`), pose le lien du thème et avertit si l'utilisateur `sddm` ne peut pas lire le home.
**Dépendances** : aucune (le nettoyage de `screenlayout.d/` est déclaré hors périmètre)
**Fichier** : `.specs/backlog/2026-11-05-861406-feature-install_sddm.md`

#### 3. `9cf61c` — Dispositions d'écran par machine

**Type** : feature
**Domaine** : qtile / écrans
**Chantier** : divers
**Objectif** : nouveau script `bin/screenlayout` (menu rofi limité à la machine courante via `uname -n`, et `--default`), lien `screenlayout.d/sddm` remplacé par un script qui lance `screenlayout --default`, disposition par défaut appliquée aussi par `autostart.sh`.
**Dépendances** : `8d134c` et `861406` — déclarées explicitement (« s'implémente après … ; part de l'état qu'elles laissent »)
**Fichier** : `.specs/backlog/2026-11-05-9cf61c-feature-dispositions_ecran_par_machine.md`

---

## 3. Ordre global recommandé

```
1. 8d134c — Nettoyage des écrans [divers] (draft, déblocant pour 9cf61c)
2. 861406 — Groupe sddm d'install-arch-deps.sh [divers] (draft, déblocant pour 9cf61c)
3. 9cf61c — Dispositions d'écran par machine [divers] (draft, dépend de 8d134c et 861406)
```

Pourquoi cet ordre :

- `9cf61c` passe en dernier : c'est la seule dépendance déclarée, et elle porte sur les deux autres.
- Entre `8d134c` et `861406`, aucune dépendance. `8d134c` passe d'abord : purement soustractif (suppressions, aucun comportement ajouté), il réduit `screenlayout.d/` et `keybindings.py`/`commands.py` avant que les deux features y touchent, et sa spec décrit déjà l'état « lien `sddm` gardé pour SDDM » que `861406` exploite.
- Alternative acceptable : `861406` puis `8d134c`. Les deux se touchent seulement sur `install-arch-deps.sh` (commentaire du groupe `screens` contre nouveau groupe `sddm`) et `.config/qtile/CLAUDE.md` (sections différentes) — conflits textuels mineurs, pas de conflit de fond.

## 5. Notes et risques

- **`abhoth.sh` existe déjà** (commit `89d8901`) mais `8d134c` a été écrite avant : son test `ls screenlayout.d/` attend « exactement `arandr`, `daoloth.sh`, `sddm` ». Il faut le lire comme « plus `abhoth.sh` », qui ne doit **pas** être supprimé (il n'est pas dans la liste des suppressions, et `9cf61c` le suppose présent).
- **Noms de fichiers de `8d134c`** : la spec liste `alien-thin` et `alien-sam-pip-right`, alors que les fichiers réels sont `alien-thin.sh` et `alien-sam-pip-right.sh`. Même cible, extension à ajuster au `git rm`.
- **`daoloth.sh` commenté deux fois** : `861406` y ajoute un commentaire (« lancé via le lien `sddm`… ne pas renommer le lien »), puis `9cf61c` transforme ce lien en script et réécrit le commentaire. `9cf61c` doit remplacer le commentaire de `861406`, pas l'empiler ; la règle 5 de `861406` (`sddm` exécutable) reste satisfaite par le script.
- **Documentation partagée** : les trois specs modifient `.config/qtile/CLAUDE.md` (section « Monitor Configuration » pour `8d134c` et `9cf61c`) et deux d'entre elles `CLAUDE.md` racine. Implémenter dans l'ordre évite que `9cf61c` décrive un état que `8d134c` n'a pas encore produit.
- **Vérifications réelles** : SDDM (thème, `chmod o+x` sur le laptop) et le menu ne se valident que sur les machines daoloth et abhoth ; les tests du dépôt reposent sur des faux `sudo`, `pacman`, `systemctl`, `uname`, `rofi`.

## Commandes utiles

```bash
# Implémenter une spec
kda-work {hash}

# Rédiger une spec manquante
kda-spec {description}

# Mettre à jour ce plan
kda-plan
```
