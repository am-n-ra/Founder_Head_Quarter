# FHQ CLI — v1 (M0 structure + M1 traçabilité)

Implémentation de référence des deux premiers jalons du plan (`fhq-plan-v1.md`).

## Installation
```
pip install pyyaml
```

## Utilisation
```bash
# Initialiser un repo fhq
python3 -m fhq_cli.cli init ./fhq --owner "Ton Nom"

# Créer une venture (Phase 0 automatique)
python3 -m fhq_cli.cli venture new ./fhq credo --archetype fintech_reglemente

# Créer un produit sous cette venture
python3 -m fhq_cli.cli product new ./fhq credo credo-app

# Voir l'état actuel (paliers, checklist du gate en cours)
python3 -m fhq_cli.cli status ./fhq credo

# Cocher un critère (déclenche un commit git attribué)
python3 -m fhq_cli.cli check ./fhq credo hypothese_utilisateur_precis
python3 -m fhq_cli.cli check ./fhq credo hypothese_problem_precis
python3 -m fhq_cli.cli check ./fhq credo exemple_concret

# Tenter de franchir le gate — avance automatiquement si tous les must-meet sont cochés
python3 -m fhq_cli.cli advance ./fhq credo

# Enregistrer une décision structurante (ADR)
python3 -m fhq_cli.cli decision new ./fhq credo "Titre" \
  --contexte "..." --decision "..." --auteur "Toi"

# Reconstituer l'historique d'une venture, 10 ans plus tard
git -C ./fhq log --follow -- ventures/credo/venture.yaml
```

## Ce qui est implémenté (M0 + M1 + M2 + M3 du plan)
- Hiérarchie Venture → Produit → Projet (`fhq_cli/core.py`)
- Squelette complet des 8 phases / paliers / gates de la formule (`fhq_cli/schema.py`)
- Cochage de critères must-meet/should-meet, avec franchissement automatique de gate
- Chaque changement d'état réel = un commit git attribué (auteur + horodatage natifs)
- Décisions structurantes au format ADR (`/decisions/*.yaml`)
- Bibliothèque des 6 archétypes branchée (`fhq_cli/archetypes.py`) — affichée dans `status`
- Calibrage novice/vétéran (`fhq niveau`)
- Fast-track (`fhq fast-track`) — gate sauté consciemment, critères non validés restent visibles, jamais supprimés
- Programme du jour agrégé (`fhq programme`) et détection de silence/relance proactive (`fhq silence`)
- `SKILL.md` — point d'entrée agnostique lisible par tout agent, avec déclencheur `/fhq`, et la même logique programme/silence explicitée en prose pour un agent sans exécution de code (parité fonctionnelle CLI ↔ skill)

## Nouvelles commandes (M3)
```bash
python3 -m fhq_cli.cli programme ./fhq   # agrégé, priorisé, toutes ventures actives
python3 -m fhq_cli.cli silence ./fhq     # ventures en retard sur leur cadence attendue
```

## Pas encore implémenté (M4-M5)
- Le repo public `founderhq` distribuable n'existe pas encore (celui-ci est un dossier de travail)
- Auto-découverte des ventures-équipe, progressive disclosure, Issues/Discussions liées aux gates
- Couche astro (Swiss Ephemeris), matching opportunités par tags
