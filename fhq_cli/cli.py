#!/usr/bin/env python3
"""
CLI FHQ v1 (M0 + M1).
Usage :
    fhq init <chemin> --owner "Nom"
    fhq venture new <chemin> <nom> [--archetype X] [--equipe]
    fhq product new <chemin> <venture> <produit>
    fhq project new <chemin> <venture> <produit> <projet> --remote <url>
    fhq check <chemin> <venture> <cle_critere> [--produit X] [--defait]
    fhq advance <chemin> <venture> [--produit X]
    fhq decision new <chemin> <venture> <titre> --contexte "..." --decision "..." [--alternatives "..."] [--auteur "..."] [--inflexion]
    fhq status <chemin> <venture> [--produit X]
"""

import argparse
import json
from pathlib import Path

from . import core


def main():
    parser = argparse.ArgumentParser(prog="fhq")
    sub = parser.add_subparsers(dest="commande", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("chemin")
    p_init.add_argument("--owner", required=True)

    p_venture = sub.add_parser("venture")
    venture_sub = p_venture.add_subparsers(dest="action", required=True)
    v_new = venture_sub.add_parser("new")
    v_new.add_argument("chemin")
    v_new.add_argument("nom")
    v_new.add_argument("--archetype", default=None)
    v_new.add_argument("--equipe", action="store_true")

    p_product = sub.add_parser("product")
    product_sub = p_product.add_subparsers(dest="action", required=True)
    pr_new = product_sub.add_parser("new")
    pr_new.add_argument("chemin")
    pr_new.add_argument("venture")
    pr_new.add_argument("produit")

    p_project = sub.add_parser("project")
    project_sub = p_project.add_subparsers(dest="action", required=True)
    proj_new = project_sub.add_parser("new")
    proj_new.add_argument("chemin")
    proj_new.add_argument("venture")
    proj_new.add_argument("produit")
    proj_new.add_argument("projet")
    proj_new.add_argument("--remote", required=True)

    p_check = sub.add_parser("check")
    p_check.add_argument("chemin")
    p_check.add_argument("venture")
    p_check.add_argument("cle_critere")
    p_check.add_argument("--produit", default=None)
    p_check.add_argument("--defait", action="store_true")

    p_advance = sub.add_parser("advance")
    p_advance.add_argument("chemin")
    p_advance.add_argument("venture")
    p_advance.add_argument("--produit", default=None)

    p_decision = sub.add_parser("decision")
    decision_sub = p_decision.add_subparsers(dest="action", required=True)
    d_new = decision_sub.add_parser("new")
    d_new.add_argument("chemin")
    d_new.add_argument("venture")
    d_new.add_argument("titre")
    d_new.add_argument("--contexte", required=True)
    d_new.add_argument("--decision", required=True)
    d_new.add_argument("--alternatives", default="")
    d_new.add_argument("--auteur", default="")
    d_new.add_argument("--inflexion", action="store_true")

    p_niveau = sub.add_parser("niveau")
    p_niveau.add_argument("chemin")
    p_niveau.add_argument("ventures_precedentes", type=int)

    p_fasttrack = sub.add_parser("fast-track")
    p_fasttrack.add_argument("chemin")
    p_fasttrack.add_argument("venture")
    p_fasttrack.add_argument("--justification", required=True)
    p_fasttrack.add_argument("--facteurs", required=True)
    p_fasttrack.add_argument("--produit", default=None)

    p_programme = sub.add_parser("programme")
    p_programme.add_argument("chemin")

    p_silence = sub.add_parser("silence")
    p_silence.add_argument("chemin")

    p_status = sub.add_parser("status")
    p_status.add_argument("chemin")
    p_status.add_argument("venture")
    p_status.add_argument("--produit", default=None)

    args = parser.parse_args()
    fhq_path = Path(args.chemin) if hasattr(args, "chemin") else None

    if args.commande == "init":
        core.init_fhq_repo(fhq_path, args.owner)
        print(f"fhq initialisé dans {fhq_path}")

    elif args.commande == "venture" and args.action == "new":
        core.new_venture(fhq_path, args.nom, archetype=args.archetype, equipe=args.equipe)
        print(f"venture '{args.nom}' créée — Phase 0")

    elif args.commande == "product" and args.action == "new":
        core.new_product(fhq_path, args.venture, args.produit)
        print(f"produit '{args.produit}' créé pour '{args.venture}' — Phase 0")

    elif args.commande == "project" and args.action == "new":
        core.new_project(fhq_path, args.venture, args.produit, args.projet, args.remote)
        print(f"projet '{args.projet}' référencé -> {args.remote}")

    elif args.commande == "check":
        core.check_criterion(fhq_path, args.venture, args.cle_critere,
                              fait=not args.defait, produit=args.produit)
        print(f"critère '{args.cle_critere}' -> {'fait' if not args.defait else 'défait'}")

    elif args.commande == "advance":
        result = core.try_advance_gate(fhq_path, args.venture, produit=args.produit)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.commande == "decision" and args.action == "new":
        path = core.new_decision(
            fhq_path, args.venture, args.titre, args.contexte, args.decision,
            alternatives=args.alternatives, auteur=args.auteur, inflexion=args.inflexion,
        )
        print(f"décision enregistrée -> {path}")

    elif args.commande == "niveau":
        niveau = core.set_niveau(fhq_path, args.ventures_precedentes)
        print(f"niveau calibré -> {niveau}")

    elif args.commande == "fast-track":
        result = core.fast_track(fhq_path, args.venture, args.justification, args.facteurs, produit=args.produit)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.commande == "programme":
        result = core.programme_du_jour(fhq_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.commande == "silence":
        result = core.ventures_silencieuses(fhq_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.commande == "status":
        result = core.show_status(fhq_path, args.venture, produit=args.produit)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
