"""
Coeur de FHQ v1 (M0 structure + M1 traçabilité).
Écrit/lit les fichiers YAML de la hiérarchie Venture -> Produit -> Projet,
et committe chaque changement d'état réel (jamais une simple lecture).
"""

import subprocess
import datetime
from pathlib import Path
from dataclasses import asdict

import yaml

from .schema import get_phase, PHASES
from .archetypes import get_archetype


# ---------- utilitaires git ----------

def _git(fhq_path: Path, *args):
    result = subprocess.run(
        ["git", "-C", str(fhq_path), *args],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} a échoué : {result.stderr}")
    return result.stdout.strip()


def _commit(fhq_path: Path, message: str, files: list[str]):
    _git(fhq_path, "add", *files)
    # rien à committer si aucun changement réel (ex: relecture) -> ne pas planter
    status = _git(fhq_path, "status", "--porcelain")
    if not status:
        return None
    _git(fhq_path, "commit", "-m", message)
    return _git(fhq_path, "rev-parse", "HEAD")


# ---------- initialisation du repo fhq ----------

def init_fhq_repo(fhq_path: Path, owner_name: str):
    fhq_path.mkdir(parents=True, exist_ok=True)
    (fhq_path / "ventures").mkdir(exist_ok=True)
    (fhq_path / "decisions").mkdir(exist_ok=True)

    index = {"owner": owner_name, "ventures": []}
    _write_yaml(fhq_path / "index.yaml", index)

    prefs = {"niveau": "non_defini", "ventures_precedentes": None}
    _write_yaml(fhq_path / "preferences.yaml", prefs)

    if not (fhq_path / ".git").exists():
        _git(fhq_path, "init")
        _git(fhq_path, "config", "user.email", "fhq@local")
        _git(fhq_path, "config", "user.name", owner_name)

    _commit(fhq_path, "init: repo fhq initialisé", ["index.yaml", "preferences.yaml"])
    return fhq_path


def _write_yaml(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def _read_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# ---------- état de phase initial (Phase 0, tous critères non faits) ----------

def _phase_state_initial() -> dict:
    phase0 = get_phase(0)
    return {
        "phase_actuelle": 0,
        "palier_actuel": phase0.paliers[0].id,
        "paliers": {
            p.id: {"nom": p.nom, "clos": False}
            for p in phase0.paliers
        },
        "gate_criteres": {
            **{c.cle: False for c in phase0.gate_sortie.must_meet},
            **{c.cle: False for c in phase0.gate_sortie.should_meet},
        },
    }


# ---------- venture ----------

def new_venture(fhq_path: Path, nom: str, archetype: str | None = None, equipe: bool = False):
    venture_dir = fhq_path / "ventures" / nom
    if venture_dir.exists():
        raise FileExistsError(f"La venture '{nom}' existe déjà")

    venture_data = {
        "nom": nom,
        "archetype": archetype,
        "equipe": equipe,
        "vision": None,
        "mission": None,
        "north_star": None,
        "phase_state": _phase_state_initial(),
    }
    _write_yaml(venture_dir / "venture.yaml", venture_data)
    (venture_dir / "decisions").mkdir(parents=True, exist_ok=True)
    (venture_dir / "products").mkdir(parents=True, exist_ok=True)

    index = _read_yaml(fhq_path / "index.yaml")
    index.setdefault("ventures", []).append({
        "nom": nom, "phase_actuelle": 0, "archetype": archetype,
    })
    _write_yaml(fhq_path / "index.yaml", index)

    rel = str(venture_dir.relative_to(fhq_path))
    _commit(
        fhq_path,
        f"venture({nom}): création — Phase 0 initialisée",
        [rel, "index.yaml"],
    )
    return venture_dir


def new_product(fhq_path: Path, venture: str, produit: str):
    product_dir = fhq_path / "ventures" / venture / "products" / produit
    if product_dir.exists():
        raise FileExistsError(f"Le produit '{produit}' existe déjà pour '{venture}'")

    product_data = {
        "nom": produit,
        "venture": venture,
        "phase_state": _phase_state_initial(),
    }
    _write_yaml(product_dir / "product.yaml", product_data)
    (product_dir / "documents").mkdir(parents=True, exist_ok=True)
    (product_dir / "projects").mkdir(parents=True, exist_ok=True)

    rel = str(product_dir.relative_to(fhq_path))
    _commit(
        fhq_path,
        f"produit({venture}/{produit}): création — Phase 0 initialisée",
        [rel],
    )
    return product_dir


def new_project(fhq_path: Path, venture: str, produit: str, projet: str, remote_url: str):
    project_dir = fhq_path / "ventures" / venture / "products" / produit / "projects" / projet
    if project_dir.exists():
        raise FileExistsError(f"Le projet '{projet}' existe déjà")

    _write_yaml(project_dir / "project.yaml", {"nom": projet, "produit": produit, "venture": venture})
    _write_yaml(project_dir / "remote.yaml", {"remote_url": remote_url, "type": "reference"})

    rel = str(project_dir.relative_to(fhq_path))
    _commit(
        fhq_path,
        f"projet({venture}/{produit}/{projet}): référence ajoutée -> {remote_url}",
        [rel],
    )
    return project_dir


# ---------- cocher un critère (déclenche l'écriture + commit) ----------

def _target_file(fhq_path: Path, venture: str, produit: str | None) -> Path:
    if produit:
        return fhq_path / "ventures" / venture / "products" / produit / "product.yaml"
    return fhq_path / "ventures" / venture / "venture.yaml"


def check_criterion(fhq_path: Path, venture: str, cle_critere: str, fait: bool = True, produit: str | None = None):
    target = _target_file(fhq_path, venture, produit)
    if not target.exists():
        raise FileNotFoundError(f"Introuvable : {target}")

    data = _read_yaml(target)
    gate_criteres = data.setdefault("phase_state", {}).setdefault("gate_criteres", {})
    if cle_critere not in gate_criteres:
        raise KeyError(
            f"Critère '{cle_critere}' inconnu pour la phase actuelle. "
            f"Critères disponibles : {list(gate_criteres.keys())}"
        )
    gate_criteres[cle_critere] = fait
    _write_yaml(target, data)

    rel = str(target.relative_to(fhq_path))
    scope = f"{venture}/{produit}" if produit else venture
    etat = "fait" if fait else "défait"
    return _commit(fhq_path, f"palier({scope}): critère '{cle_critere}' marqué {etat}", [rel])


def try_advance_gate(fhq_path: Path, venture: str, produit: str | None = None):
    """Vérifie si tous les must-meet du gate courant sont cochés ; si oui, avance à la phase suivante."""
    target = _target_file(fhq_path, venture, produit)
    data = _read_yaml(target)
    state = data["phase_state"]
    phase_actuelle = state["phase_actuelle"]
    phase = get_phase(phase_actuelle)
    gate = phase.gate_sortie

    if gate is None:
        return {"avance": False, "raison": "Dernière phase — pas de gate de sortie"}

    must_meet_ok = all(state["gate_criteres"].get(c.cle, False) for c in gate.must_meet)
    if not must_meet_ok:
        manquants = [c.cle for c in gate.must_meet if not state["gate_criteres"].get(c.cle, False)]
        return {"avance": False, "raison": f"Critères must-meet manquants : {manquants}"}

    nouvelle_phase = get_phase(phase_actuelle + 1)
    state["phase_actuelle"] = nouvelle_phase.numero
    state["palier_actuel"] = nouvelle_phase.paliers[0].id
    state["paliers"] = {p.id: {"nom": p.nom, "clos": False} for p in nouvelle_phase.paliers}
    if nouvelle_phase.gate_sortie:
        state["gate_criteres"] = {
            **{c.cle: False for c in nouvelle_phase.gate_sortie.must_meet},
            **{c.cle: False for c in nouvelle_phase.gate_sortie.should_meet},
        }
    else:
        state["gate_criteres"] = {}

    data["phase_state"] = state
    _write_yaml(target, data)

    rel = str(target.relative_to(fhq_path))
    scope = f"{venture}/{produit}" if produit else venture
    _commit(
        fhq_path,
        f"gate({scope}): {gate.id} franchi -> Phase {nouvelle_phase.numero} ({nouvelle_phase.nom})",
        [rel],
    )
    return {"avance": True, "nouvelle_phase": nouvelle_phase.numero, "nom": nouvelle_phase.nom}


# ---------- calibrage novice/vétéran ----------

def set_niveau(fhq_path: Path, ventures_precedentes: int):
    prefs = _read_yaml(fhq_path / "preferences.yaml")
    niveau = "novice" if ventures_precedentes <= 0 else ("intermediaire" if ventures_precedentes <= 2 else "veteran")
    prefs["ventures_precedentes"] = ventures_precedentes
    prefs["niveau"] = niveau
    _write_yaml(fhq_path / "preferences.yaml", prefs)
    _commit(fhq_path, f"onboarding: niveau calibré -> {niveau}", ["preferences.yaml"])
    return niveau


def get_niveau(fhq_path: Path) -> str:
    prefs = _read_yaml(fhq_path / "preferences.yaml")
    return prefs.get("niveau", "non_defini")


# ---------- fast-track (saut conscient d'un gate) ----------

def fast_track(fhq_path: Path, venture: str, justification: str, facteurs: str, produit: str | None = None):
    """Marque le gate courant comme sauté consciemment. Reste tracé 'différé, non validé'
    plutôt que supprimé — le risque ne disparaît pas, il devient visible."""
    if not justification.strip():
        raise ValueError("Fast-track exige une justification écrite — refusé si vide")

    target = _target_file(fhq_path, venture, produit)
    data = _read_yaml(target)
    state = data["phase_state"]
    phase = get_phase(state["phase_actuelle"])
    gate = phase.gate_sortie
    if gate is None:
        raise ValueError("Pas de gate de sortie à cette phase")

    state.setdefault("fast_tracks", []).append({
        "gate_id": gate.id,
        "justification": justification,
        "facteurs": facteurs,
        "criteres_non_valides": [
            c.cle for c in gate.must_meet if not state["gate_criteres"].get(c.cle, False)
        ],
        "statut": "differe_non_valide",
    })

    nouvelle_phase = get_phase(phase.numero + 1)
    state["phase_actuelle"] = nouvelle_phase.numero
    state["palier_actuel"] = nouvelle_phase.paliers[0].id
    state["paliers"] = {p.id: {"nom": p.nom, "clos": False} for p in nouvelle_phase.paliers}
    if nouvelle_phase.gate_sortie:
        state["gate_criteres"] = {
            **{c.cle: False for c in nouvelle_phase.gate_sortie.must_meet},
            **{c.cle: False for c in nouvelle_phase.gate_sortie.should_meet},
        }

    data["phase_state"] = state
    _write_yaml(target, data)

    rel = str(target.relative_to(fhq_path))
    scope = f"{venture}/{produit}" if produit else venture
    _commit(
        fhq_path,
        f"fast-track({scope}): {gate.id} sauté consciemment -> Phase {nouvelle_phase.numero} ({nouvelle_phase.nom}) — différé, non validé",
        [rel],
    )
    return {"phase": nouvelle_phase.numero, "statut": "differe_non_valide"}


# ---------- programme du jour + relance proactive (M3) ----------

def _dernier_commit_touchant(fhq_path: Path, rel_path: str) -> datetime.datetime | None:
    out = _git(fhq_path, "log", "-1", "--format=%aI", "--", rel_path)
    if not out:
        return None
    return datetime.datetime.fromisoformat(out)


def programme_du_jour(fhq_path: Path) -> list[dict]:
    """Agrège, à travers toutes les ventures actives, les critères manquants du gate
    courant, priorisés par proximité du gate (moins de critères manquants = plus prioritaire)."""
    from .schema import get_phase as _gp

    index = _read_yaml(fhq_path / "index.yaml")
    items = []
    for v in index.get("ventures", []):
        nom = v["nom"]
        venture_file = fhq_path / "ventures" / nom / "venture.yaml"
        if not venture_file.exists():
            continue
        data = _read_yaml(venture_file)
        state = data["phase_state"]
        phase = _gp(state["phase_actuelle"])
        if phase.gate_sortie is None:
            continue
        manquants = [c.cle for c in phase.gate_sortie.must_meet if not state["gate_criteres"].get(c.cle, False)]
        if manquants:
            items.append({
                "venture": nom,
                "phase": phase.numero,
                "nom_phase": phase.nom,
                "criteres_manquants": manquants,
                "nb_manquants": len(manquants),
            })
    items.sort(key=lambda x: x["nb_manquants"])
    return items


def ventures_silencieuses(fhq_path: Path) -> list[dict]:
    """Compare le rythme observé (dernier commit touchant la venture) au rythme
    attendu pour sa phase actuelle. Retourne les ventures en retard sur leur cadence."""
    from .schema import get_phase as _gp, CADENCE_ATTENDUE_JOURS

    index = _read_yaml(fhq_path / "index.yaml")
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    resultats = []
    for v in index.get("ventures", []):
        nom = v["nom"]
        venture_dir = fhq_path / "ventures" / nom
        venture_file = venture_dir / "venture.yaml"
        if not venture_file.exists():
            continue
        data = _read_yaml(venture_file)
        phase_num = data["phase_state"]["phase_actuelle"]
        rel = str(venture_dir.relative_to(fhq_path))
        dernier = _dernier_commit_touchant(fhq_path, rel)
        if dernier is None:
            continue
        jours_ecoules = (maintenant - dernier).days
        cadence = CADENCE_ATTENDUE_JOURS.get(phase_num, 7)
        if jours_ecoules > cadence:
            resultats.append({
                "venture": nom,
                "phase": phase_num,
                "jours_depuis_derniere_activite": jours_ecoules,
                "cadence_attendue_jours": cadence,
            })
    return resultats


# ---------- décisions (ADR) ----------

def new_decision(fhq_path: Path, venture: str, titre: str, contexte: str, decision: str,
                  alternatives: str = "", auteur: str = "", inflexion: bool = False):
    slug = titre.lower().replace(" ", "-")
    date = datetime.date.today().isoformat()
    filename = f"{date}-{slug}.yaml"
    decisions_dir = fhq_path / "ventures" / venture / "decisions"
    decisions_dir.mkdir(parents=True, exist_ok=True)
    path = decisions_dir / filename

    adr = {
        "date": date,
        "auteur": auteur,
        "titre": titre,
        "contexte": contexte,
        "decision": decision,
        "alternatives_considerees": alternatives,
        "type": "inflexion" if inflexion else "decision",
    }
    _write_yaml(path, adr)

    rel = str(path.relative_to(fhq_path))
    tag = "inflexion" if inflexion else "decision"
    _commit(fhq_path, f"{tag}({venture}): {titre}", [rel])
    return path


# ---------- statut ----------

def show_status(fhq_path: Path, venture: str, produit: str | None = None) -> dict:
    target = _target_file(fhq_path, venture, produit)
    data = _read_yaml(target)
    state = data["phase_state"]
    phase = get_phase(state["phase_actuelle"])

    checklist = []
    if phase.gate_sortie:
        for c in phase.gate_sortie.must_meet:
            checklist.append({"cle": c.cle, "desc": c.description, "type": "must-meet",
                               "fait": state["gate_criteres"].get(c.cle, False)})
        for c in phase.gate_sortie.should_meet:
            checklist.append({"cle": c.cle, "desc": c.description, "type": "should-meet",
                               "fait": state["gate_criteres"].get(c.cle, False)})

    archetype_cle = data.get("archetype")
    archetype = get_archetype(archetype_cle) if archetype_cle else None

    return {
        "venture": venture,
        "produit": produit,
        "phase": phase.numero,
        "nom_phase": phase.nom,
        "question_centrale": phase.question_centrale,
        "paliers": list(state["paliers"].keys()),
        "checklist_gate": checklist,
        "fast_tracks_en_attente": state.get("fast_tracks", []),
        "niveau_utilisateur": get_niveau(fhq_path),
        "archetype": {
            "nom": archetype.nom,
            "preuve_pmf_dominante": archetype.preuve_pmf_dominante,
            "vecteur_distribution_typique": archetype.vecteur_distribution_typique,
            "piege_phase5": archetype.piege_phase5,
        } if archetype else None,
    }
