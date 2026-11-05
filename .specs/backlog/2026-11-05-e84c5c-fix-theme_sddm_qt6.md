# Écran de login noir sur le laptop : porter le thème SDDM fdt2k-dark en Qt 6

Status: draft
Chantier: divers

## Situation initiale

Le thème SDDM `fdt2k-dark` est versionné dans `.local/share/sddm/themes/fdt2k-dark/`. C'est une copie du thème **Sugar Dark** (`metadata.desktop` : `Theme-Id=sugar-dark`, `Theme-API=2.11`), écrit pour **Qt 5**. Le groupe `sddm` d'`install-arch-deps.sh` (spec `861406`, [archive](../archives/2026-11-05-861406-feature-install_sddm.md)) :
- le lie depuis `/usr/share/sddm/themes/fdt2k-dark` ;
- le choisit dans `/etc/sddm.conf.d/10-dotfiles.conf` (`[Theme] Current=fdt2k-dark`).

Les deux machines ont `sddm 0.21.0-7`. Avec SDDM 0.21, c'est le thème qui décide de l'écran de login lancé : `QtVersion=6` dans `metadata.desktop` → `sddm-greeter-qt6` ; sinon → `sddm-greeter`, la version Qt 5.

| Machine | Écrans de login installés |
|---|---|
| fixe (daoloth) | `/usr/bin/sddm-greeter`, `/usr/bin/sddm-greeter-qt6` |
| laptop (abhoth) | `sddm-greeter-qt6` seulement (`sddm-greeter` introuvable) |

Le QML du thème importe des modules Qt 5 :
- `QtGraphicalEffects 1.0` dans `Main.qml`, `Components/Input.qml`, `Components/UserList.qml` et `Components/SessionButton.qml`, pour les `DropShadow` (`layer.effect`) ;
- des imports versionnés : `QtQuick 2.11`, `QtQuick.Controls 2.4`, `QtQuick.Layouts 1.11`, `QtQuick.VirtualKeyboard 2.3`, `SddmComponents 2.0`.

## Problème

- **Symptôme** : sur le laptop, après `install-arch-deps.sh sddm`, l'écran de login reste noir avec un curseur immobile. Journal de SDDM :
  ```
  Starting X11 session: "" "/usr/bin/sddm-greeter --socket … --theme /usr/share/sddm/themes/fdt2k-dark"
  Auth: sddm-helper exited with 127
  Greeter stopped. SDDM::Auth::HelperExitStatus(127)
  ```
- **Déclencheur** : un thème sans `QtVersion=6`, sur une machine sans écran de login Qt 5. Code 127 : commande introuvable.
- **Impact** : pas d'écran de login sur le laptop. Le fixe ne fonctionne que parce qu'il a encore l'écran de login Qt 5, que les installations récentes n'ont plus.

## Comportement attendu

1. Le thème déclare **`QtVersion=6`** dans la section `[SddmGreeterTheme]` de `metadata.desktop`. SDDM lance alors `sddm-greeter-qt6` sur les deux machines.
2. Le QML se charge sous Qt 6 :
   - `import QtGraphicalEffects 1.0` → **`import Qt5Compat.GraphicalEffects`** dans les 4 fichiers. Les `DropShadow` restent identiques.
   - les imports versionnés de Qt (`QtQuick`, `QtQuick.Controls`, `QtQuick.Layouts`, `QtQuick.VirtualKeyboard`) perdent leur numéro de version, facultatif en Qt 6 ;
   - `SddmComponents 2.0` et `import "Components"` restent tels quels.
3. Le groupe `sddm` d'`install-arch-deps.sh` installe les modules Qt 6 dont le thème a besoin : **`qt6-5compat`** (`Qt5Compat.GraphicalEffects`), **`qt6-svg`** (icônes `Assets/*.svgz`), **`qt6-virtualkeyboard`** (`Components/VirtualKeyboard.qml`), avec `sddm`.
4. Rendu inchangé : mêmes couleurs, même mise en page, mêmes ombres, mêmes réglages lus dans `theme.conf` et `theme.conf.user`.

> Invariants : même thème pour les deux machines ; aucune modification de `theme.conf` ni de `bin/theme/sddm`.

## Comportement actuel (avant fix)

- `grep -c QtVersion metadata.desktop` → 0.
- `grep -rl "import QtGraphicalEffects" .` → 4 fichiers.
- Laptop : `sddm-helper exited with 127`, écran noir.

## Cause identifiée

- `.local/share/sddm/themes/fdt2k-dark/metadata.desktop` — pas de `QtVersion=6` : SDDM 0.21 choisit l'écran de login Qt 5, absent du laptop.
- `Main.qml`, `Components/Input.qml`, `Components/UserList.qml`, `Components/SessionButton.qml` — `QtGraphicalEffects` n'existe plus en Qt 6 : même lancé en Qt 6, le thème ne se chargerait pas.
- `.config/qtile/bin/install-arch-deps.sh` — le groupe `sddm` n'installe pas les modules Qt 6 dont le thème a besoin.

## Solution

### `metadata.desktop`

Ajouter `QtVersion=6` dans `[SddmGreeterTheme]`, par exemple après `Theme-API=2.11`. Aucune autre ligne ne change.

### QML

- `Main.qml`, `Components/Input.qml`, `Components/UserList.qml`, `Components/SessionButton.qml` : `import QtGraphicalEffects 1.0` → `import Qt5Compat.GraphicalEffects`.
- Tous les fichiers QML : `import QtQuick 2.11` → `import QtQuick`, `import QtQuick.Controls 2.4` → `import QtQuick.Controls`, `import QtQuick.Layouts 1.11` → `import QtQuick.Layouts`, `import QtQuick.VirtualKeyboard 2.3` → `import QtQuick.VirtualKeyboard`.
- Aucune autre ligne de QML ne change. Si une incompatibilité Qt 6 apparaît au test de l'humain (`sddm-greeter-qt6 --test-mode`, voir Tests), elle fera l'objet d'une correction séparée, avec le message d'erreur.

### `install-arch-deps.sh`

`SDDM_PKGS=(sddm qt6-5compat qt6-svg qt6-virtualkeyboard)`, et le commentaire du tableau mis à jour (modules Qt 6 du thème).

### Documentation

`.config/qtile/CLAUDE.md` (ligne du groupe `sddm`) : le thème est en Qt 6 (`QtVersion=6`) ; le groupe installe les modules Qt 6 du thème.

## Contraintes à respecter

- Ne pas modifier `theme.conf`, `theme.conf.user`, les images, les `Assets/`, ni la logique QML (positions, couleurs, textes, ombres).
- Ne pas toucher au reste de `setup_sddm`.
- Dépôts officiels seulement.

## Tests

Le dépôt n'a pas de suite de tests (`## Tests` du `CLAUDE.md`), et le container n'a ni Qt ni SDDM. Les vérifications sont statiques dans la session, puis faites par l'humain avec le mode test de l'écran de login, qui ouvre le thème dans une fenêtre sans toucher à SDDM.

| Cas | Attendu |
|-----|---------|
| Reproduit le bug — avant fix, `grep -c '^QtVersion=6' metadata.desktop` / `grep -rl 'import QtGraphicalEffects' .local/share/sddm/themes/fdt2k-dark` | 0 / 4 fichiers |
| Après fix, `grep -c '^QtVersion=6' metadata.desktop` | 1, dans la section `[SddmGreeterTheme]` |
| Après fix, `grep -rn 'QtGraphicalEffects\|import QtQuick[.A-Za-z]* [0-9]' .local/share/sddm/themes/fdt2k-dark` | aucun résultat |
| Après fix, `grep -rl 'import Qt5Compat.GraphicalEffects'` | les 4 fichiers |
| `git diff` des fichiers QML | uniquement des lignes `import` |
| `install-arch-deps.sh sddm` (faux `sudo`) | pacman reçoit `sddm qt6-5compat qt6-svg qt6-virtualkeyboard` |
| Laptop — `sddm-greeter-qt6 --test-mode --theme ~/.local/share/sddm/themes/fdt2k-dark` (depuis la session) | le thème s'ouvre dans une fenêtre, sans erreur QML dans le terminal |
| Laptop — `sudo systemctl restart sddm`, puis `Ctrl+Alt+F2` | écran de login Sugar Dark |
| Fixe — même test en mode test, puis au prochain démarrage | écran de login inchangé, désormais en Qt 6 |
