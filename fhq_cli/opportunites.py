"""
Matching opportunités <-> palier actuel, par tags — pas de moteur sémantique.
Réutilise le vocabulaire déjà défini dans schema.py (opportunites_pertinentes par gate).
Source : fhq-architecture-v1.md, section 9.
"""

from pathlib import Path
import yaml

from .schema import get_phase


def ajouter_opportunite(fhq_path: Path, titre: str, type_tag: str, description: str = ""):
    """Entrée manuelle v1 — pas de scan web automatique."""
    opp_dir = fhq_path / "opportunites"
    opp_dir.mkdir(exist_ok=True)
    slug = titre.lower().replace(" ", "-")
    path = opp_dir / f"{slug}.yaml"
    data = {"titre": titre, "type": type_tag, "description": description, "matchee": False}
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    return path


def matcher_opportunites(fhq_path: Path) -> list[dict]:
    """Croise chaque opportunité stockée avec le palier actuel de chaque venture active."""
    opp_dir = fhq_path / "opportunites"
    index_path = fhq_path / "index.yaml"
    if not opp_dir.exists() or not index_path.exists():
        return []

    with open(index_path, encoding="utf-8") as f:
        index = yaml.safe_load(f) or {}

    opportunites = []
    for opp_file in opp_dir.glob("*.yaml"):
        with open(opp_file, encoding="utf-8") as f:
            opportunites.append({"fichier": opp_file, **(yaml.safe_load(f) or {})})

    correspondances = []
    for v in index.get("ventures", []):
        venture_file = fhq_path / "ventures" / v["nom"] / "venture.yaml"
        if not venture_file.exists():
            continue
        with open(venture_file, encoding="utf-8") as f:
            vdata = yaml.safe_load(f) or {}
        phase_num = vdata.get("phase_state", {}).get("phase_actuelle", 0)
        phase = get_phase(phase_num)
        if phase.gate_sortie is None:
            continue
        tags_pertinents = set(phase.gate_sortie.opportunites_pertinentes)

        for opp in opportunites:
            if opp.get("type") in tags_pertinents:
                correspondances.append({
                    "venture": v["nom"],
                    "phase": phase_num,
                    "opportunite": opp["titre"],
                    "type": opp["type"],
                })

    return correspondances
