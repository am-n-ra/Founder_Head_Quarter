# FounderHQ — PRD (Product Requirements Document) v1

> Consolide `fhq-formule-phases-v1.md` (le QUOI) et `fhq-architecture-v1.md` (le COMMENT) en spec actionnable — user stories et critères d'acceptation, pour que n'importe quel contributeur (humain ou agent IA) puisse construire sans deviner.

---

## 1. Vision produit

FounderHQ est une source de vérité unique, git-native, ouverte à tous, qui guide n'importe quel porteur de projet — novice ou vétéran, seul ou en équipe, sur n'importe quelle venture — à travers une formule générale de phases éprouvée, sans jamais se demander "où j'en suis, d'où je viens, où je vais". Open-source, accessible via n'importe quel outil IA, sans app dédiée.

**Pour qui :** tout fondateur/porteur de projet dans le monde, quel que soit l'archétype de venture (SaaS, marketplace, infra/deep-tech, fintech réglementé, commerce physique, service/agence).

**Ce que ce n'est pas :** un CRM, un outil de gestion de projet générique, un chatbot de conseil startup. C'est un système d'état persistant qui sait exactement où en est chaque venture et ce qu'il faut faire ensuite, avec preuve à l'appui.

---

## 2. Épopées (Epics) et user stories

### Épopée A — Installation et onboarding

**US-A1** : En tant qu'utilisateur, je veux pouvoir dire "install fhq" à n'importe quel agent IA (Claude Code, OpenCode, ChatGPT, Gemini) et obtenir une installation fonctionnelle.
- *Critères d'acceptation* : l'agent trouve le repo `founderhq` par recherche web, lit `INSTALL.md`/`AGENTS.md`, exécute automatiquement si l'agent a accès terminal, sinon guide pas-à-pas ; résultat = repo privé `fhq` généré et structuré.

**US-A2** : En tant que nouvel utilisateur, je veux que l'onboarding détermine mon niveau (novice/vétéran) sans questionnaire lourd.
- *Critères d'acceptation* : une question simple (nombre de ventures précédentes portées) ; le calibrage s'ajuste ensuite selon le comportement observé.

**US-A3** : En tant qu'utilisateur activant la couche astrologie, je veux que mon thème natal sidéral soit calculé avec précision professionnelle.
- *Critères d'acceptation* : calcul via Swiss Ephemeris, ayanamsa Lahiri par défaut (autre système sélectionnable), résultat stocké dans `astro-profile.yaml`. Fonctionnalité entièrement optionnelle — l'onboarding fonctionne sans si l'utilisateur ne l'active pas.

### Épopée B — Structurer une venture

**US-B1** : En tant qu'utilisateur, je veux créer une nouvelle venture et que le système la place automatiquement en Phase 0 (Étincelle).
- *Critères d'acceptation* : `venture.yaml` généré avec structure Phase 0, Palier 0.1 ouvert.

**US-B2** : En tant qu'utilisateur, je veux qu'une venture puisse avoir plusieurs produits, chacun avec son propre état de phase.
- *Critères d'acceptation* : structure `products/<produit>/product.yaml` indépendante ; deux produits d'une même venture peuvent afficher des phases différentes simultanément.

**US-B3** : En tant qu'utilisateur, je veux que chaque produit puisse référencer plusieurs projets/repos de code sans dupliquer le code.
- *Critères d'acceptation* : `projects/<projet>/remote.yaml` contient un pointeur (URL ou submodule), jamais une copie du code.

### Épopée C — Progresser dans la formule

**US-C1** : En tant qu'utilisateur, je veux voir clairement mon palier actuel, ce qui est déjà validé, et ce qu'il manque pour avancer.
- *Critères d'acceptation* : affichage en checklist (chaque critère must-meet/should-meet individuellement coché/non coché) — jamais un état binaire caché.

**US-C2** : En tant qu'utilisateur, je veux que le système applique l'archétype de ma venture pour adapter les critères de gate concrets.
- *Critères d'acceptation* : le contenu affiché (preuve de PMF attendue, vecteur de distribution suggéré) varie selon l'archétype choisi (SaaS, Marketplace, Infra/Deep-tech, Fintech réglementé, Commerce physique, Service/Agence), le squelette Phase/Palier/Gate reste identique.

**US-C3** : En tant qu'utilisateur novice, je veux que le système déroule l'éventail complet des canaux de distribution possibles ; en tant que vétéran, je veux pouvoir tester directement mon hypothèse.
- *Critères d'acceptation* : comportement conditionné par le calibrage novice/vétéran de l'onboarding (US-A2).

**US-C4** : En tant qu'utilisateur, je ne veux jamais être bloqué de façon punitive si un gate échoue — je veux comprendre ce qui a changé.
- *Critères d'acceptation* : un gate non franchi est présenté comme "nouvelle information : [X] invalide [hypothèse]", jamais comme "vous reculez" ou "échec".

**US-C5** : En tant qu'utilisateur avec un contexte spécifique (marché massif, effets réseau), je veux pouvoir sauter consciemment un gate.
- *Critères d'acceptation* : statut "Fast-track" activable, exige une justification écrite ; le gate sauté reste marqué "différé, non validé" en arrière-plan, jamais supprimé.

### Épopée D — Travailler en équipe

**US-D1** : En tant qu'utilisateur invité comme collaborateur sur une venture d'un autre utilisateur, je veux qu'elle apparaisse automatiquement dans mon FHQ sans action manuelle.
- *Critères d'acceptation* : auto-découverte via marqueur `fhq-venture` + accès GitHub réel de l'utilisateur ; ajout automatique dans `index.yaml`.

**US-D2** : En tant que membre d'une équipe, je veux savoir qui fait quoi sur un palier donné, sans que ça encombre l'expérience solo.
- *Critères d'acceptation* : champs propriétaire/validateur/échéance invisibles par défaut en solo, apparaissent automatiquement dès l'ajout d'un second collaborateur (progressive disclosure).

**US-D3** : En tant qu'équipe, je veux discuter d'un palier/gate précis sans outil de chat séparé.
- *Critères d'acceptation* : Issues/Discussions GitHub natifs scopés au palier/gate concerné, liés à l'ADR qu'ils produisent le cas échéant.

### Épopée E — Traçabilité et mémoire longitudinale

**US-E1** : En tant qu'utilisateur, je veux pouvoir remonter, des années plus tard, pourquoi une décision a été prise.
- *Critères d'acceptation* : chaque décision structurante génère un fichier ADR (`/decisions/*.yaml`) avec contexte, décision, alternatives considérées, auteur, date.

**US-E2** : En tant qu'utilisateur, je veux que les événements imprévisibles (Inflexions) soient capturés même s'ils n'étaient pas planifiés.
- *Critères d'acceptation* : même format ADR avec marqueur `type: inflexion`, capturable à tout moment quelle que soit la phase en cours.

**US-E3** : En tant qu'utilisateur, je ne veux pas que la traçabilité ralentisse mon exécution quotidienne.
- *Critères d'acceptation* : l'écriture ne se déclenche que sur un changement d'état réel (palier, gate, décision) — jamais sur une simple question/discussion.

### Épopée F — Guidage quotidien proactif

**US-F1** : En tant qu'utilisateur, je veux un programme du jour sans avoir à le construire moi-même.
- *Critères d'acceptation* : calculé à la volée à partir de l'état réel (paliers ouverts, must-meet manquants) à travers toutes les ventures actives, priorisé.

**US-F2** : En tant qu'utilisateur, je veux être relancé si une venture reste silencieuse trop longtemps par rapport à sa phase.
- *Critères d'acceptation* : comparaison rythme observé (horodatage natif) vs rythme attendu par phase ; relance proactive à la prochaine interaction, sans que l'utilisateur ait à le demander.

**US-F3** : En tant qu'utilisateur ayant activé l'astrologie, je veux que le calendrier calibre le *moment* des actions nécessaires.
- *Critères d'acceptation* : `/calendar.yaml` traduit les actions prioritaires en créneaux, calibrés par le thème natal — jamais utilisé pour décider *si* une action est nécessaire, seulement *quand*.

### Épopée G — Opportunités externes

**US-G1** : En tant qu'utilisateur, je veux qu'une opportunité externe pertinente pour mon palier actuel me soit signalée, même si je ne savais pas qu'elle existait.
- *Critères d'acceptation* : matching par tags entre l'opportunité (entrée manuelle en v1) et le champ "opportunités pertinentes" du palier actuel ; remontée via le même mécanisme que US-F2.

**US-G2** : En tant qu'utilisateur, je veux pouvoir demander une recherche ponctuelle (concurrents, financement, validation) à tout moment.
- *Critères d'acceptation* : l'agent IA exécute une recherche web à la demande, dans la conversation — disponible dès la v1, indépendamment du matching automatique différé.

---

## 3. Hors scope v1 (explicitement différé)

- Découverte automatique et continue d'opportunités par scan web en arrière-plan (US-G1 reste manuel en v1)
- Validation historique approfondie au-delà des cas déjà traités (recherche continue, pas un livrable v1)
- Dashboard applicatif dédié (le rendu passe par `README.md` auto-généré, natif GitHub)
- Moteur de calibrage de seuils de saturation entièrement personnalisé dès le premier usage (cold start = a priori par archétype, affiné ensuite)

---

## 4. Dépendances techniques clés

- Git/GitHub (repos, permissions, Issues/Discussions, rendu markdown natif)
- git/SSH/`gh` CLI pour les opérations routinières ; serveur MCP GitHub officiel pour l'orchestration riche (avec allow-listing)
- Swiss Ephemeris (AGPL) pour le calcul astro sidéral
- Agent IA avec capacité de recherche web native pour US-G2

---

## 5. Métriques de succès du produit (pas de la venture individuelle)

- Un utilisateur peut installer FHQ et créer sa première venture en moins de 10 minutes, dans n'importe quel agent IA compatible
- Un utilisateur en équipe ne fait jamais d'action manuelle pour rejoindre une venture à laquelle il a accès
- Aucune décision structurante n'est perdue — 100% des décisions marquées comme telles génèrent une ADR retrouvable
- Le programme du jour est généré sans intervention manuelle de configuration à chaque session
