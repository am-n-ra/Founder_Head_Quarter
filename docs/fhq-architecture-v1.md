# FounderHQ — Architecture technique (v1)

> Compagnon du document `fhq-formule-phases-v1.md`. La formule définit QUOI guider ; ce document définit COMMENT c'est stocké, accédé, partagé, et tracé.
> Principe directeur : s'appuyer sur ce que git/GitHub font déjà nativement, plutôt que reconstruire une infrastructure custom.
> Statut : v1 complète, tous les points ouverts tranchés.

---

## 1. Choix fondamental — Git-natif plutôt que base de données hébergée

FHQ n'utilise pas de base de données centrale traditionnelle (type Supabase/Postgres) comme source de vérité principale. À la place : **des repos git**, structurés, qui portent à la fois le code des produits ET l'état de la formule.

**Pourquoi ce choix plutôt qu'un backend classique :**
- La traçabilité longitudinale (10 ans) est native à git — pas à construire
- Le code des ventures reste où il est déjà (pas de duplication/désynchronisation)
- Les outils IA savent déjà parler à des repos git (Claude Code, Cursor, GitHub Copilot, serveur MCP officiel GitHub) — agnosticisme résolu sans développement custom
- La collaboration multi-utilisateur (permissions, rôles, revue) est un système déjà mature chez GitHub — pas à recoder
- Coût de départ : zéro

**Limite assumée :** pas de dashboard temps réel out-of-the-box comme un vrai backend applicatif — nécessite une fine couche de rendu/lecture par-dessus (voir section 6).

---

## 2. Distribution / installation

Un repo template public : **`founderhq`**.

- N'importe qui, n'importe où dans le monde, peut l'installer (fork/clone via un script d'installation)
- L'installation génère un repo privé personnel : **`fhq`**, structuré selon le squelette ci-dessous
- Ce repo privé est le tableau de bord personnel de l'utilisateur — ses ventures solo y vivent directement ; ses ventures en équipe y sont référencées

---

## 3. Hiérarchie de données — Venture → Produit → Projet

```
fhq/                              (repo perso — dashboard/index)
├── index.yaml                    (vue d'ensemble légère : liste des ventures, phase actuelle, 1 ligne résumé chacune)
├── astro-profile.yaml            (thème natal du founder, calculé à l'onboarding)
├── preferences.yaml              (novice/vétéran, calibrage général)
│
└── ventures/
    ├── <venture-solo>/            (venture solo → dossier direct dans le repo perso)
    │   ├── venture.yaml           (vision/mission/north star, état de phase niveau venture)
    │   ├── decisions/              (ADR — voir section 5)
    │   └── products/
    │       └── <produit>/
    │           ├── product.yaml   (état de phase — spécifique à CE produit)
    │           ├── documents/     (exec summary, business plan, PRD, roadmap, etc.)
    │           └── projects/
    │               └── <projet>/
    │                   ├── project.yaml
    │                   └── remote.yaml   (lien vers le repo de code réel, ou submodule git)
    │
    └── <venture-equipe>.ref.yaml  (référence légère — la venture réelle vit dans son propre repo partagé)
```

Une **venture-équipe** vit dans son propre repo distinct (ex: `credo-fhq`), avec collaborateurs GitHub natifs (permissions lecture/écriture/admin par personne). Le repo perso de chaque membre ne contient qu'une référence (`*.ref.yaml` avec l'URL du repo partagé) — pas de duplication.

**Auto-découverte, pas d'ajout manuel.** Un repo venture-équipe porte un marqueur reconnaissable (tag GitHub `fhq-venture`, ou fichier `.fhq-venture.yaml` à sa racine). Dès qu'un utilisateur a accès à un repo marqué comme tel (parce qu'il y a été invité comme collaborateur), FHQ le détecte via l'API GitHub et ajoute automatiquement la référence dans `index.yaml` — à l'installation, et en continu ensuite. Quelqu'un présent dans 15 ventures différentes n'ajoute jamais rien à la main.

**Lecture à la demande, jamais de téléchargement complet.** Le `*.ref.yaml` ne contient qu'un pointeur. Le contenu réel (état des paliers, documents) est lu via l'API GitHub/MCP seulement quand l'IA ou l'utilisateur en a besoin — pas de clone local systématique. Ça évite la question "il faut tout télécharger un par un" : il n'y a jamais rien à télécharger en bloc.

**Pourquoi l'état de phase existe à 3 niveaux (venture/produit/projet) :** une venture peut avoir un produit en Phase 4 (PMF) et un autre encore en Phase 1 (Discovery) simultanément — le niveau venture reflète une vue agrégée, mais la vérité opérationnelle est au niveau produit.

---

## 4. Contexte progressif — comment l'IA navigue sans se noyer

Chaque niveau de dossier porte un fichier **index léger** (résumé, quelques lignes) et des fichiers **détail complets** (chargés seulement à la demande) — le même principe qu'une mémoire IA bien conçue : une liste résumée pour savoir où regarder, puis lecture complète seulement du fichier pertinent.

| Niveau | Ce que l'IA voit par défaut | Ce qu'elle charge en descendant |
|---|---|---|
| Racine (`fhq/`) | `index.yaml` — toutes les ventures, phase actuelle, 1 ligne chacune | — |
| `/ventures/<x>/` | `venture.yaml` — vision, état complet des paliers de cette venture | Documents, décisions si besoin |
| `/products/<y>/` | `product.yaml` — état détaillé de ce produit spécifique | Documents produit, projets |
| `/projects/<z>/` | `project.yaml` + `remote.yaml` | Le code réel, via le lien/submodule |

Ça permet de gérer un nombre arbitraire de ventures/produits/projets sans jamais saturer une seule fenêtre de contexte IA.

---

## 5. Traçabilité longitudinale — mémoire sur 10 ans

Aucun système de tracking séparé. Tout repose sur ce que git fournit nativement (auteur + horodatage sur chaque commit) plus une convention structurée pour les décisions.

**Changements d'état (routine)**
Chaque palier qui avance = un commit sur `*.yaml` (product.yaml, venture.yaml). L'historique git de ce fichier est la timeline exacte de progression, interrogeable via `git log` / `git blame`.

**Décisions (structurantes)**
Format **ADR (Architecture Decision Record)**, un fichier par décision dans `/decisions/` :
```yaml
# /decisions/2026-07-11-choix-canal-distribution.yaml
date: 2026-07-11
auteur: <qui>
contexte: <ce qui a motivé la décision>
decision: <ce qui a été choisi>
alternatives_considerees: <ce qui a été écarté et pourquoi>
lien_discussion: <URL de l'Issue/Discussion GitHub liée, si applicable>
```

**Inflexions (événements imprévisibles)**
Même format ADR, avec un marqueur `type: inflexion` — capturées dès qu'elles surviennent, quelle que soit la phase en cours, reliées à ce qui a changé dans la trajectoire ensuite.

**Communication d'équipe**
Issues/Discussions GitHub natifs, scopés à un palier/gate précis (référencé dans le nom ou les labels de l'Issue). Déjà horodatés et attribués nativement — liés à l'ADR qu'ils ont produit plutôt que dupliqués.

---

## 6. Guidage quotidien — programme et cadence proactive

Pas de programme stocké à l'avance : **calculé à la volée** à partir de l'état réel.

- **Le "programme du jour"** = pour chaque venture/produit actif, quel palier est en cours, quels must-meet manquent, quelle est l'action la plus proche → agrégé et priorisé à travers toutes les ventures de l'utilisateur
- **Calendrier optionnel** — `/calendar.yaml` ou synchro externe, où les actions prioritaires se traduisent en créneaux ; c'est ici que la couche astro se branche (calibrage du *moment*, jamais du *si*)
- **Suivi proactif** — le système compare le rythme d'activité observé (horodatage natif des commits/messages) par venture au rythme attendu pour sa phase. Une venture silencieuse au-delà de ce qui est cohérent déclenche une relance à la prochaine interaction, sans attendre que l'utilisateur y pense

---

## 7. Couche astrologie — où elle se branche exactement

Jamais dans les critères de gate eux-mêmes (qui restent basés sur des preuves réelles). Elle intervient à deux points précis :
- **Onboarding** : calcul du thème natal (sidéral), stocké dans `astro-profile.yaml`
- **Calibrage temporel** : quel jour/moment tenter une action déjà nécessaire (lancement, réunion clé, palier à franchir) — dans `/calendar.yaml`

**Note sur l'ayanamsa Lahiri** : c'est un standard astronomique (point de référence sur l'étoile Spica), pas un cadre culturel — adopté officiellement par l'Inde en 1956, mais devenu la référence sidérale la plus testée et documentée mondialement, indépendamment du contexte de l'utilisateur. Swiss Ephemeris supporte 40+ systèmes d'ayanamsa ; Lahiri est proposé par **défaut** (le plus précis/éprouvé), le choix reste ouvert à l'onboarding si un utilisateur préfère un autre système (Fagan-Bradley, Krishnamurti, Raman, etc.).

---

## 8. Boucle opérationnelle — comment un message devient un commit

C'est le mécanisme concret qui relie la conversation avec l'IA à l'état persistant du repo. **Chaque message qui produit un changement d'état réel** (un palier avancé, un critère coché, une décision prise) déclenche cette séquence :

1. **Identifier le(s) fichier(s) concerné(s)** — quel `product.yaml`/`venture.yaml`/`decisions/*.yaml` est affecté par ce qui vient d'être dit
2. **Écrire directement dans ce fichier** — pas de stockage intermédiaire, le fichier structuré EST la source de vérité
3. **Committer avec un message descriptif** — auteur et horodatage sont natifs à git, le message de commit résume le changement (convention proche de : `palier(credo/1.3): early believer confirmé — X`)
4. **Régénérer les vues dérivées si besoin** — le `README.md` auto-généré (section 6) se met à jour pour rester cohérent avec l'état réel

Une simple question ou discussion n'écrit rien — seul un changement d'état réel (palier, gate, décision) déclenche l'écriture. C'est le même principe qu'une mémoire IA bien conçue : on n'écrit pas à chaque échange, on écrit quand un fait durable apparaît.

---

## 9. Mécanisme de matching opportunités ↔ palier

Matching par tags, pas de moteur sémantique complexe — réutilise la taxonomie déjà définie dans la formule plutôt que d'en construire une nouvelle.

1. Chaque opportunité (levée, accélérateur, partenariat) est taguée avec le même vocabulaire que le champ "opportunités pertinentes ici" des gates (`type: pre-seed`, `type: accelerateur`, `type: partenariat-big-fish`, etc.)
2. Le système croise ces tags avec le palier **actuel** de chaque venture/produit actif de l'utilisateur
3. Une correspondance déclenche une remontée proactive — le même mécanisme que la cadence quotidienne (section 6), pas un système séparé

**V1 : entrée manuelle des opportunités** (utilisateur ou équipe les ajoute), matching automatique par tags. **Hors scope v1** : découverte automatique par scan web *continu en arrière-plan* — fonctionnalité v2 légitime, mais ajoute une dépendance de recherche/filtrage non nécessaire pour valider le mécanisme de base.

**Recherche web à la demande — disponible dès la v1.** À ne pas confondre avec le scan automatique différé ci-dessus : l'agent IA qui pilote FHQ a nativement accès à la recherche web (Claude, ou tout agent équivalent). Dès la v1, l'utilisateur peut demander une recherche ponctuelle — concurrents pour Palier 1.1, validation Phase 3.2, opportunités de financement pour l'archétype en cours — et l'IA l'exécute à la volée, dans la conversation. Ce qui est différé en v2, c'est uniquement le scan *automatique et permanent* qui tournerait sans que l'utilisateur le demande.

---

## Résolu dans cette session

- **Accès outils IA** : git/SSH/`gh` CLI en direct par défaut pour les opérations routinières (léger, universel) ; serveur MCP GitHub officiel réservé à l'orchestration plus riche (Issues/PR/workflows), avec allow-listing pour limiter le coût de contexte (le serveur complet charge ~42-55K tokens de schéma à lui seul)
- **Rendu visuel** : pas d'app séparée — `README.md` auto-généré à partir des fichiers YAML à chaque commit, affiché nativement par GitHub dans le navigateur ou tout IDE
- **Calcul astro** : Swiss Ephemeris (Astrodienst) comme moteur, ayanamsa Lahiri comme référence sidérale standard
- **Boucle message → fichier → commit** : confirmée et détaillée en section 8
- **Décision de licence** : FHQ est open-source (AGPL, cohérent avec l'intégration de Swiss Ephemeris). La monétisation se fait par-dessus — hébergement géré, support, fonctionnalités premium — pas par la fermeture du code. Open-source et modèle commercial ne s'excluent pas (cf. GitLab, Supabase).
- **Mécanisme d'installation** : le repo `founderhq` contient un fichier d'entrée standardisé (`INSTALL.md`/`AGENTS.md`) écrit pour être lu et exécuté par un agent IA, pas seulement par un humain. Dire "install fhq" dans n'importe quel agent (Claude Code, OpenCode, ChatGPT, Gemini) déclenche : recherche web → repo trouvé → lecture du fichier d'entrée → exécution automatique si l'agent a accès terminal/fichiers, ou guidage pas-à-pas si l'agent n'a que le chat. Même point d'entrée, mode d'exécution adapté aux capacités de l'outil — même principe que les fichiers SKILL.md.

**Correction importante — FHQ est un repo-skill, pas un package à installer.** Le cœur de FHQ (schéma des phases, règles de progression, format des fichiers) vit dans un `SKILL.md` en langage structuré que n'importe quel agent lit et applique avec ses propres outils natifs (lire/écrire fichiers, exécuter git) — sans dépendance externe (pas de Python/pip requis). Ça garantit l'agnosticisme réel : un agent chat-only sans exécution de code peut quand même appliquer FHQ, juste en suivant les instructions et en éditant les fichiers YAML lui-même. Un CLI (comme celui livré en v1, section 8bis) reste disponible comme **couche de confort optionnelle** pour les agents avec exécution de code — plus rapide, moins d'erreurs de format — mais jamais un prérequis.
