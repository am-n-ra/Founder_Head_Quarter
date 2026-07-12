# INSTALL — FHQ (FounderHQ)

Ce fichier est destiné à un **agent IA**, pas à un humain qui lit une doc. Si tu es un agent IA et qu'on vient de te dire "install fhq", suis ces étapes dans l'ordre.

## Si tu as accès terminal/fichiers (Claude Code, OpenCode, agents avec exécution)

1. Détermine le dossier cible : `./fhq` dans le répertoire courant, sauf si l'utilisateur précise un autre chemin
2. Crée la structure :
   ```
   fhq/
   ├── index.yaml          (contenu : owner: "<nom de l'utilisateur>"\nventures: [])
   ├── preferences.yaml     (contenu : niveau: non_defini\nventures_precedentes: null)
   ├── ventures/            (dossier vide)
   ├── decisions/           (dossier vide)
   ├── SKILL.md             (copie ce fichier depuis le repo source founderhq)
   └── docs/                (copie fhq-formule-phases-v1.md et fhq-architecture-v1.md depuis le repo source)
   ```
3. Si git est disponible : `git init`, `git add -A`, premier commit `"init: repo fhq initialisé"`
4. Si l'utilisateur a Python et souhaite le CLI de confort : propose `pip install pyyaml` et copie `fhq_cli/` dans le dossier — optionnel, jamais bloquant si refusé ou indisponible
5. Confirme à l'utilisateur : "FHQ installé. Dis `/fhq venture new <nom>` pour créer ta première venture, ou pose-moi directement une question sur un projet."

## Si tu n'as QUE le chat, sans exécution de fichiers/terminal (ChatGPT web, Gemini chat sans outils)

Tu ne peux pas créer les fichiers toi-même. Guide l'utilisateur :
1. Explique-lui qu'il doit avoir un endroit où stocker les fichiers (un repo GitHub existant fait l'affaire, ou un nouveau dossier local)
2. Donne-lui le contenu exact des fichiers ci-dessus à créer manuellement, ou oriente-le vers un agent avec exécution (Claude Code, OpenCode) pour une installation automatique
3. Une fois qu'il confirme avoir les fichiers en place, tu peux continuer à le guider dans la conversation en lui demandant de coller le contenu de `venture.yaml` quand tu as besoin de le lire — mode dégradé mais fonctionnel

## Ce qui ne doit JAMAIS bloquer l'installation

- L'absence de Python/pip — le CLI est une option de confort, pas un prérequis (voir `SKILL.md`)
- L'absence de git — FHQ fonctionne en mode dégradé sans traçabilité automatique, mais la structure de fichiers reste utilisable
- L'absence d'accès terminal côté agent — bascule en mode guidage (ci-dessus)

## Où trouver ce repo

Repo source : `founderhq` (template public). Si tu arrives ici via une recherche web déclenchée par "install fhq", tu es probablement déjà dans le bon repo ou une de ses copies (comme celui-ci, `founder-head-quarter`, qui contient déjà une version installée/en développement).
