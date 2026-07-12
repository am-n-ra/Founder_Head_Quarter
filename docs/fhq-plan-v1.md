# FounderHQ — Plan de développement (v1)

> Séquence le PRD (`fhq-prd-v1.md`) en jalons exécutables et ordonnés. Principe : valider le noyau le plus vite possible (solo, une venture, sans équipe ni astro) avant d'empiler les couches optionnelles.

---

## Logique de séquencement

Trois raisons gouvernent l'ordre :
1. **Le modèle de données doit exister avant tout le reste** — impossible de construire guidage ou traçabilité sur une structure qui bouge encore
2. **Le solo avant l'équipe** — la collaboration (Épopée D) ajoute une complexité (permissions, auto-découverte) qu'il ne faut pas porter avant que le noyau solo soit validé
3. **L'optionnel après l'essentiel** — astro (US-A3) et opportunités (Épopée G) sont des couches qui se branchent sur un système déjà fonctionnel, pas des prérequis

---

## M0 — Noyau : structure de données + une venture solo

**Contenu :** Épopée B en entier (US-B1, B2, B3) + squelette minimal de l'Épopée C (US-C1 uniquement — afficher l'état, sans encore l'archétype ni le calibrage novice/vétéran)

**Objectif :** un utilisateur peut créer une venture, voir sa Phase 0 s'afficher, cocher un critère manuellement, et voir le fichier YAML se mettre à jour.

**Definition of done :** `venture.yaml` généré et lisible, structure Produit/Projet fonctionnelle, un critère de palier peut être marqué fait/pas fait et c'est visible.

**Dépendances :** aucune — c'est le point de départ.

---

## M1 — Traçabilité (le mécanisme d'écriture)

**Contenu :** Épopée E en entier (US-E1, E2, E3) + section 8 de l'architecture (boucle message → fichier → commit)

**Objectif :** chaque changement d'état sur M0 déclenche un commit correctement attribué ; les décisions structurantes génèrent une ADR.

**Definition of done :** modifier un critère de palier produit un commit git avec auteur/horodatage/message cohérent ; une décision marquée comme telle crée un fichier dans `/decisions/`.

**Dépendances :** M0 (il faut des fichiers à versionner).

> **Pourquoi si tôt dans le plan :** la traçabilité n'est pas une fonctionnalité qu'on ajoute après coup — si elle arrive après que l'utilisateur ait déjà avancé dans plusieurs paliers, l'historique reconstitué a posteriori. Elle doit être active dès le premier changement d'état réel.

---

## M2 — Formule complète : archétypes, calibrage, gates réels

**Contenu :** reste de l'Épopée C (US-C2, C3, C4, C5) + la bibliothèque d'archétypes de `fhq-formule-phases-v1.md`

**Objectif :** le système applique les critères concrets par archétype, adapte le niveau de guidage (novice/vétéran), refuse un gate de façon non-punitive, permet le Fast-track justifié.

**Definition of done :** deux ventures de deux archétypes différents affichent des critères de gate différents pour le même palier générique ; un gate raté affiche le message reformulé (pas "échec") ; un Fast-track avec justification est possible et reste tracé comme "différé, non validé".

**Dépendances :** M0, M1 (les critères doivent s'écrire quelque part de tracé).

---

## M3 — Guidage quotidien proactif

**Contenu :** Épopée F en entier (US-F1, F2) — F3 (calendrier astro) déplacé en M5 avec le reste de l'astro

**Objectif :** un programme du jour se calcule automatiquement à partir de l'état réel ; une venture silencieuse trop longtemps déclenche une relance.

**Definition of done :** ouvrir une session avec plusieurs ventures actives affiche un résumé priorisé sans configuration manuelle ; une venture artificiellement mise en pause déclenche une relance à la session suivante.

**Dépendances :** M2 (le calcul du programme a besoin des critères de gate réels, pas juste de l'affichage brut de M0).

---

## M4 — Installation agent-native

**Contenu :** Épopée A en entier SAUF astro (US-A1, A2) — le fichier `INSTALL.md`/`AGENTS.md`, le repo template public `founderhq`

**Objectif :** n'importe qui peut dire "install fhq" dans un agent IA compatible et obtenir un `fhq` fonctionnel qui contient déjà M0-M3.

**Definition of done :** test réel dans au moins deux agents différents (un avec exécution terminal type Claude Code, un chat-only type ChatGPT web) — les deux arrivent à un résultat installé ou à un guidage complet.

**Dépendances :** M0-M3 (il faut quelque chose de stable à installer).

> **Pourquoi si tard :** l'installation n'a de valeur que si ce qu'elle installe fonctionne déjà. La construire avant M0-M3 reviendrait à distribuer une coquille vide.

---

## M5 — Couches optionnelles : équipe, astro, opportunités

**Contenu :** Épopée D en entier (US-D1, D2, D3) + US-A3 (astro) + US-F3 (calendrier astro) + Épopée G (US-G1, G2)

**Objectif :** les fonctionnalités qui se branchent sur un système déjà solide, sans en être des prérequis.

**Definition of done (par sous-bloc, livrables indépendamment) :**
- Équipe : auto-découverte fonctionnelle, progressive disclosure des champs propriétaire/validateur, Issues/Discussions liés aux gates
- Astro : calcul Swiss Ephemeris fonctionnel, calibrage calendrier branché sans influencer les gates eux-mêmes
- Opportunités : matching par tags fonctionnel sur entrée manuelle ; recherche web à la demande (US-G2, techniquement disponible dès que l'agent IA a l'outil — peut être activé dès M0 en pratique, formalisé ici)

**Dépendances :** M0-M4 (ce sont des extensions, pas des fondations).

---

## Vue d'ensemble des dépendances

```
M0 (structure)
  └─→ M1 (traçabilité)
        └─→ M2 (formule complète)
              └─→ M3 (guidage quotidien)
                    └─→ M4 (installation)
                          └─→ M5 (équipe / astro / opportunités)
```

Séquence strictement linéaire par design — chaque jalon dépend du précédent, cohérent avec le principe de la formule elle-même (pas de gate sauté sans justification). Si un Fast-track s'impose (ex: paralléliser M4 et le début de M5 équipe), il doit être justifié explicitement, exactement comme le prévoit le mécanisme Fast-track qu'on a conçu pour les utilisateurs de FHQ — cohérence entre comment on construit FHQ et ce que FHQ prescrit.

---

## Prochaine étape suggérée

M0 est prêt à être spécifié techniquement en détail (schéma YAML exact, validation de structure) puis développé. C'est le point d'entrée naturel pour la phase "Dev" du méta-process.
