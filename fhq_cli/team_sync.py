"""
Auto-découverte des ventures-équipe via l'API GitHub.
Source : fhq-architecture-v1.md, section 3.

Ce module ne peut pas être testé en sandbox sans authentification GitHub réelle —
l'interface est complète et prête, les appels API sont documentés précisément
pour qu'un agent avec accès `gh`/token les exécute directement.
"""

from pathlib import Path
import yaml
import subprocess
import json


MARQUEUR_VENTURE_EQUIPE = "fhq-venture"  # tag GitHub attendu sur les repos ventures-équipe


def lister_repos_marques(utilisateur_gh: str | None = None) -> list[dict]:
    """
    Utilise `gh` CLI (déjà authentifié côté utilisateur) pour lister les repos
    auxquels l'utilisateur a accès et qui portent le tag 'fhq-venture'.

    Commande réelle exécutée :
        gh search repos --topic fhq-venture --json name,owner,url

    Si `gh` n'est pas disponible, retourne une liste vide plutôt que de planter —
    l'auto-découverte est une amélioration, pas un prérequis (cf. INSTALL.md).
    """
    try:
        result = subprocess.run(
            ["gh", "search", "repos", "--topic", MARQUEUR_VENTURE_EQUIPE,
             "--json", "name,owner,url"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return []
        return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return []


def synchroniser_ventures_equipe(fhq_path: Path) -> list[str]:
    """
    Compare les repos marqués fhq-venture accessibles à l'utilisateur avec ce qui
    est déjà référencé dans index.yaml, et ajoute automatiquement les manquants
    comme des '<nom>.ref.yaml' (référence légère, pas de clone du contenu).

    Retourne la liste des nouvelles ventures découvertes cette exécution.
    """
    index_path = fhq_path / "index.yaml"
    with open(index_path, encoding="utf-8") as f:
        index = yaml.safe_load(f) or {"ventures": []}

    deja_connues = {v["nom"] for v in index.get("ventures", [])}
    repos = lister_repos_marques()

    nouvelles = []
    for repo in repos:
        nom = repo.get("name")
        if not nom or nom in deja_connues:
            continue

        ref_path = fhq_path / "ventures" / f"{nom}.ref.yaml"
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ref_path, "w", encoding="utf-8") as f:
            yaml.safe_dump({
                "nom": nom,
                "type": "venture_equipe_reference",
                "remote_url": repo.get("url"),
                "proprietaire": repo.get("owner", {}).get("login"),
            }, f, allow_unicode=True, sort_keys=False)

        index.setdefault("ventures", []).append({"nom": nom, "type": "reference"})
        nouvelles.append(nom)

    if nouvelles:
        with open(index_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(index, f, allow_unicode=True, sort_keys=False)

    return nouvelles
