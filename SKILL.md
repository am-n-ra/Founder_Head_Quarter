# FHQ (FounderHQ) — Skill

Ce fichier est destiné à être lu par un agent IA (toi). Il décrit comment appliquer la formule FounderHQ à une venture, directement avec tes outils natifs (lecture/écriture de fichiers, exécution de commandes git si disponible). Aucune dépendance externe requise — tu n'as pas besoin de Python, d'un package, ou d'un CLI pour appliquer ce skill. Si un CLI Python est présent dans ce repo (`fhq_cli/`), tu peux l'utiliser par confort si tu as l'exécution de code, mais ce n'est jamais obligatoire.

---

## Quand utiliser ce skill

- L'utilisateur tape `/fhq` suivi d'une commande ou d'une question — déclencheur explicite, prioritaire sur toute détection contextuelle
- L'utilisateur mentionne une "venture", un "produit", un "palier", une "phase", ou dit explicitement de travailler avec FHQ
- L'utilisateur demande où en est un projet, ce qu'il faut faire ensuite, ou veut enregistrer une décision
- Tu es dans un repo qui contient un dossier `ventures/` avec des fichiers `venture.yaml`

### Convention `/fhq`

```
/fhq status <venture>              → lire et afficher l'état actuel
/fhq check <venture> <critere>     → marquer un critère fait, tenter le gate
/fhq decision <venture> "<titre>"  → enregistrer une ADR (demander contexte/décision si absents)
/fhq new venture <nom>             → créer une venture, Phase 0
```
Si l'agent ne supporte pas les commandes slash nativement, traiter `/fhq ...` comme du texte brut et appliquer la même logique — le préfixe suffit à signaler l'intention.

---

## Structure des fichiers que tu dois lire/écrire

```
fhq/
├── index.yaml              # vue d'ensemble légère de toutes les ventures
├── ventures/
│   └── <nom-venture>/
│       ├── venture.yaml    # état de phase niveau venture
│       ├── decisions/      # fichiers ADR (une décision = un fichier)
│       └── products/
│           └── <produit>/
│               ├── product.yaml   # état de phase spécifique à ce produit
│               ├── documents/
│               └── projects/
│                   └── <projet>/
│                       ├── project.yaml
│                       └── remote.yaml   # pointeur vers le repo de code réel
```

## Format de `venture.yaml` / `product.yaml`

```yaml
nom: credo
archetype: fintech_reglemente   # voir liste des archétypes plus bas
vision: null
mission: null
north_star: null
phase_state:
  phase_actuelle: 0
  palier_actuel: "0.1"
  paliers:
    "0.1": {nom: "Capture du signal", clos: false}
    "0.2": {nom: "Première hypothèse", clos: false}
    "0.3": {nom: "Sacrifice", clos: false}
  gate_criteres:
    hypothese_utilisateur_precis: false
    hypothese_problem_precis: false
    exemple_concret: false
```

## Format d'une décision (`decisions/<date>-<slug>.yaml`)

```yaml
date: "2026-07-12"
auteur: <qui>
titre: <titre court>
contexte: <ce qui a motivé la décision>
decision: <ce qui a été choisi>
alternatives_considerees: <ce qui a été écarté et pourquoi>
type: decision   # ou "inflexion" pour un événement imprévisible
```

---

## Le squelette des 8 phases (universel, ne varie jamais)

| # | Phase | Question centrale |
|---|---|---|
| 0 | Étincelle | Quel problème je vis/observe, pour qui ? |
| 1 | Discovery | Ce problème est-il réel et assez douloureux pour que quelqu'un paie ? |
| 2 | Validation | Le modèle est-il reproductible ? |
| 3 | Construction | Le produit tient-il techniquement et à l'usage réel ? |
| 4 | Product-Market Fit | La rétention prouve-t-elle une demande organique ? |
| 5 | Scale | Peut-on répéter sans que tout casse ? |
| 6 | Domination | Devient-on la référence du marché ? |
| 7 | Autonomie | L'entreprise tourne-t-elle sans dépendance au fondateur ? |

Chaque phase a des paliers (jalons concrets) et un gate de sortie (critères must-meet/should-meet). **Détail complet des paliers/critères par phase : voir `docs/fhq-formule-phases-v1.md` dans ce repo — ne réinvente pas les critères, lis-les depuis ce fichier de référence.**

---

## Ce que tu dois faire, concrètement, à chaque interaction

1. **Identifier la venture/produit concerné** par la demande de l'utilisateur (lire `index.yaml` pour la liste, puis le `venture.yaml`/`product.yaml` pertinent)
2. **Répondre à la question de l'utilisateur** en te basant sur l'état lu (statut, prochaine action, checklist)
3. **Si un changement d'état réel est confirmé** (un critère rempli, une décision prise) :
   a. Modifier le fichier YAML concerné directement (édition de fichier standard)
   b. Si git est disponible : committer avec un message structuré — `palier(<venture>): critère '<cle>' marqué fait`, `gate(<venture>): <id> franchi -> Phase X`, `decision(<venture>): <titre>`
   c. Si tous les must-meet du gate courant sont maintenant vrais : faire avancer `phase_actuelle` à la phase suivante et réinitialiser `paliers`/`gate_criteres` selon le squelette de cette nouvelle phase
4. **Ne jamais committer sur une simple question** — seul un changement d'état réel déclenche l'écriture, comme une mémoire bien conçue

## Programme du jour et relance proactive — à faire sans code si besoin

Le CLI a des commandes `programme`/`silence` pour ça, mais **si tu n'as pas d'exécution de code, fais-le toi-même** en suivant exactement cette logique — le résultat doit être identique :

**Programme du jour :**
1. Lis `index.yaml` pour la liste de toutes les ventures
2. Pour chaque venture, lis `venture.yaml`, note `phase_actuelle` et les `gate_criteres` encore à `false` parmi les must-meet de cette phase (les must-meet de chaque phase sont listés dans `fhq-formule-phases-v1.md`)
3. Trie les ventures par nombre de critères manquants croissant — moins il en manque, plus c'est prioritaire (proche du gate)
4. Présente ce classement à l'utilisateur comme son programme du jour

**Détection de silence (relance proactive) :**
1. Pour chaque venture, si git est disponible : `git log -1 --format=%aI -- ventures/<nom>/venture.yaml` donne la date du dernier changement réel
2. Compare le nombre de jours écoulés à la cadence attendue pour la phase actuelle :

   | Phase | Cadence attendue (jours) |
   |---|---|
   | 0, 1 | 3 |
   | 2 | 4 |
   | 3 | 7 |
   | 4 | 5 |
   | 5 | 10 |
   | 6, 7 | 14 |

3. Si le silence dépasse la cadence attendue, relance proactivement en début de conversation — sans attendre que l'utilisateur le demande : *"[Venture] n'a pas bougé depuis [X] jours, palier [Y] toujours ouvert — on regarde ?"*
4. Sans accès git (pas de log disponible), utilise l'horodatage du dernier message de conversation portant sur cette venture comme approximation.

Cette section garantit que le comportement proactif de FHQ ne dépend jamais du CLI Python — un agent chat-only qui suit ce skill applique exactement le même raisonnement, juste sans l'automatisation du calcul.

---

## Règles de ton et de comportement

- Un gate non franchi ne se présente jamais comme un échec — toujours "nouvelle information : [X] invalide [hypothèse], à réviser"
- Un "Fast-track" (saut conscient d'un gate) exige une justification écrite explicite de l'utilisateur avant d'être appliqué ; le gate sauté reste marqué non-validé, pas supprimé
- Le contenu concret des critères (preuve de PMF attendue, vecteur de distribution) varie selon l'archétype de la venture — voir la bibliothèque d'archétypes dans `fhq-formule-phases-v1.md`
- Calibre ton niveau de guidage (déroulé complet vs hypothèse directe) selon le niveau déclaré par l'utilisateur (novice/vétéran) dans `preferences.yaml`
