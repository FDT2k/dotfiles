# Notes KDA

Remarques, idées, irritants — à trier plus tard.

---

### 2026-11-05T19h18 — commands.py : screen_layout et copyq sont des tuples

Dans `.config/qtile/qtile_config/commands.py`, `screen_layout` et `copyq` se terminent par une virgule : ce sont des tuples d'une chaîne, pas des chaînes. `lazy.spawn(command.copyq)` reçoit donc un tuple, que Qtile traite comme une liste d'arguments : il tente d'exécuter un programme nommé « …/copyq.sh » tel quel (ça peut marcher), et pour `screen_layout` un programme nommé « …/run.sh screenlayout.d "Monitor Layout" », chemin inexistant — le menu « Monitor Layout » (mod+alt+l) ne s'ouvre probablement pas. `screen_layout` sera réécrit par la spec 9cf61c ; `copyq` reste à corriger.
