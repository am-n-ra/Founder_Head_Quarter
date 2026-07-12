"""
Squelette de la formule FounderHQ — Phase -> Palier -> Gate.
Source de vérité structurelle : fhq-formule-phases-v1.md
Ce module ne contient QUE le squelette fixe (universel) ; le contenu
variable par archétype (preuve de PMF, vecteur de distribution) est
dans archetypes.py et vient se superposer, pas remplacer.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Critere:
    cle: str
    description: str
    fait: bool = False


@dataclass
class Palier:
    id: str
    nom: str
    objectif: str
    livrable: str


@dataclass
class Gate:
    id: str  # ex: "0->1"
    must_meet: List[Critere] = field(default_factory=list)
    should_meet: List[Critere] = field(default_factory=list)
    opportunites_pertinentes: List[str] = field(default_factory=list)


@dataclass
class Phase:
    numero: int
    nom: str
    question_centrale: str
    paliers: List[Palier]
    gate_sortie: Optional[Gate]  # gate vers la phase suivante ; None pour la dernière phase


def _c(cle, description):
    return Critere(cle=cle, description=description)


PHASES: List[Phase] = [
    Phase(
        numero=0,
        nom="Étincelle",
        question_centrale="Quel problème je vis/observe, pour qui ?",
        paliers=[
            Palier("0.1", "Capture du signal",
                   "Formuler l'observation/frustration initiale sans encore la juger",
                   "Note brute du problème observé"),
            Palier("0.2", "Première hypothèse",
                   "Transformer l'observation en hypothèse testable",
                   "Hypothèse formulée (qui/quoi/pourquoi/comment)"),
            Palier("0.3", "Sacrifice",
                   "Marquer un engagement irréversible",
                   "Acte non-récupérable posé (carrière/capital/réputation engagés)"),
        ],
        gate_sortie=Gate(
            id="0->1",
            must_meet=[
                _c("hypothese_utilisateur_precis", "L'hypothèse nomme un utilisateur précis (pas 'tout le monde')"),
                _c("hypothese_problem_precis", "L'hypothèse nomme un problème précis, pas une solution déguisée"),
            ],
            should_meet=[
                _c("exemple_concret", "Le fondateur peut citer un exemple concret et récent du problème"),
            ],
            opportunites_pertinentes=["ideation", "atelier_cadrage"],
        ),
    ),
    Phase(
        numero=1,
        nom="Discovery",
        question_centrale="Ce problème est-il réel et assez douloureux pour que quelqu'un paie ?",
        paliers=[
            Palier("1.1", "Sortir du bâtiment",
                   "Confronter l'hypothèse à des humains réels hors cercle proche",
                   "Liste d'entretiens avec prospects non-biaisés"),
            Palier("1.2", "Isoler le signal de douleur",
                   "Distinguer 'poli et intéressé' de 'vraiment douloureux'",
                   "Synthèse classant chaque signal (confirmé/poli/absent)"),
            Palier("1.3", "Willingness-to-pay / Early Believer",
                   "Obtenir une preuve d'engagement au-delà de la parole",
                   "Pré-vente, dépôt, lettre d'intention, ou premier chèque"),
        ],
        gate_sortie=Gate(
            id="1->2",
            must_meet=[
                _c("douleur_confirmee", "Au moins X prospects confirment la douleur sans suggestion"),
                _c("signal_wtp", "Au moins un signal de willingness-to-pay obtenu"),
            ],
            should_meet=[
                _c("marche_estimable", "Taille de marché estimable même grossièrement"),
                _c("budget_alloue_ailleurs", "Le prospect a déjà un budget alloué à ce problème ailleurs"),
            ],
            opportunites_pertinentes=["preincubation", "subvention_amorcage", "concours_pitch"],
        ),
    ),
    Phase(
        numero=2,
        nom="Validation",
        question_centrale="Le modèle est-il reproductible — pas juste un client convaincu par charisme ?",
        paliers=[
            Palier("2.1", "Formalisation du business model",
                   "Passer de l'hypothèse à un modèle testable dans son ensemble",
                   "Business model esquissé (segments, valeur, canaux, coûts/revenus)"),
            Palier("2.2", "Test de reproductibilité",
                   "Vérifier que le premier succès n'est pas un coup de chance",
                   "2e et 3e conversion obtenues par un canal répétable"),
            Palier("2.3", "Design du MVP",
                   "Définir le plus petit produit qui teste réellement la valeur",
                   "Spec du MVP (inclus/exclus et pourquoi)"),
            Palier("2.4", "Incorporation",
                   "Formaliser légalement au bon moment, pas par réflexe",
                   "Structure légale enregistrée (Day One / Trigger / Ultra tardif)"),
        ],
        gate_sortie=Gate(
            id="2->3",
            must_meet=[
                _c("conversions_reproductibles", "≥2 conversions via canal reproductible, hors réseau perso"),
                _c("modele_econ_tient", "Le modèle économique tient sur le papier (CAC < valeur générée)"),
            ],
            should_meet=[
                _c("avantage_vs_statu_quo", "Capacité à articuler l'avantage vs l'alternative précédente du prospect"),
            ],
            opportunites_pertinentes=["accelerateur_early_stage", "angels", "partenariat_pilote"],
        ),
    ),
    Phase(
        numero=3,
        nom="Construction",
        question_centrale="Le produit tient-il techniquement et à l'usage réel ?",
        paliers=[
            Palier("3.1", "Brainstorming structuré", "Explorer l'espace de solutions", "Notes de brainstorming"),
            Palier("3.2", "Recherche", "Confronter les intuitions à l'existant", "Synthèse de recherche"),
            Palier("3.3", "Spécification", "Exigences précises et non-ambiguës", "Spec fonctionnelle / cahier des charges"),
            Palier("3.4", "Architecture", "Décider comment construire avant de construire", "Document d'architecture / conception"),
            Palier("3.5", "PRD", "Unifier spec+archi en référence actionnable", "PRD / dossier de référence"),
            Palier("3.6", "Plan", "Séquencer en étapes exécutables", "Plan de développement"),
            Palier("3.7", "Dev", "Construire avec points de contrôle réguliers", "Produit fonctionnel + écarts documentés"),
        ],
        gate_sortie=Gate(
            id="3->4",
            must_meet=[
                _c("fonctionne_cas_usage_principal", "Le produit fonctionne de bout en bout pour le cas d'usage principal"),
                _c("ecarts_documentes", "Écarts PRD/réalisation documentés et justifiés"),
            ],
            should_meet=[
                _c("dette_technique_consciente", "Dette technique connue et consciente"),
                _c("test_utilisateur_externe", "Survécu à un test avec ≥1 utilisateur externe au process"),
            ],
            opportunites_pertinentes=["recrutement_technique", "infra_cout_reduit", "beta_testeurs"],
        ),
    ),
    Phase(
        numero=4,
        nom="Product-Market Fit",
        question_centrale="La rétention/traction prouve-t-elle une demande organique, pas forcée ?",
        paliers=[
            Palier("4.1", "Lancement contrôlé", "Exposer le produit à de vrais utilisateurs, mesurable", "Cohorte de lancement définie"),
            Palier("4.2", "Mesure de rétention réelle", "Distinguer curiosité et usage répété", "Données de rétention sur fenêtre significative"),
            Palier("4.3", "Preuve de demande organique", "Vérifier que la croissance ne dépend pas que du fondateur", "Signal de traction non forcée"),
        ],
        gate_sortie=Gate(
            id="4->5",
            must_meet=[
                _c("sean_ellis_40", "Sean Ellis Test ≥ 40% ('très déçu' si le produit disparaissait)"),
                _c("canal_independant", "≥1 canal d'acquisition non-dépendant du réseau personnel"),
            ],
            should_meet=[
                _c("preference_articulee", "Les utilisateurs articulent pourquoi ils préfèrent ce produit"),
                _c("recommandation_spontanee", "Signal de recommandation spontanée observé"),
            ],
            opportunites_pertinentes=["series_a", "partenariat_distribution", "presse"],
        ),
    ),
    Phase(
        numero=5,
        nom="Scale",
        question_centrale="Peut-on répéter l'acquisition/la valeur sans que tout casse ?",
        paliers=[
            Palier("5.1", "Systématisation de l'acquisition", "Transformer un canal en process reproductible", "Playbook d'acquisition documenté"),
            Palier("5.2", "Industrialisation opérationnelle", "Processus tiennent à volume supérieur", "Processus documentés, indicateurs de charge"),
            Palier("5.3", "Structuration de l'équipe", "Passer du fondateur-qui-fait-tout à une équipe", "Organigramme fonctionnel minimal"),
        ],
        gate_sortie=Gate(
            id="5->6",
            must_meet=[
                _c("rule_of_40", "Rule of 40 : croissance % + marge % ≥ 40"),
                _c("canal_scalable", "≥1 canal scalable avec économie unitaire positive ou trajectoire crédible"),
            ],
            should_meet=[
                _c("couts_ne_degradent_pas", "Coûts d'acquisition/service ne dégradent pas structurellement avec le volume"),
            ],
            opportunites_pertinentes=["series_b_plus", "expansion_geo", "acquisitions_strategiques"],
        ),
    ),
    Phase(
        numero=6,
        nom="Domination",
        question_centrale="Devient-on la référence du marché (consolidation, défensibilité) ?",
        paliers=[
            Palier("6.1", "Construction de moat", "Identifier/renforcer ce qui rend la position difficile à copier", "Cartographie des avantages défensifs"),
            Palier("6.2", "Expansion de périmètre", "Étendre la valeur sans diluer le cœur", "Feuille de route d'expansion"),
        ],
        gate_sortie=Gate(
            id="6->7",
            must_meet=[
                _c("position_leader", "Position de leader/challenger crédible et mesurable"),
                _c("avantage_defensif", "≥1 avantage défensif difficile à répliquer rapidement"),
            ],
            should_meet=[
                _c("cite_reference", "Cité comme référence par des tiers non affiliés"),
            ],
            opportunites_pertinentes=["consolidation_acquisition", "pre_ipo", "partenariats_strategiques"],
        ),
    ),
    Phase(
        numero=7,
        nom="Autonomie",
        question_centrale="L'entreprise tourne-t-elle sans dépendance critique au fondateur ?",
        paliers=[
            Palier("7.1", "Détachement opérationnel", "Vérifier que ça tourne sans intervention quotidienne", "Test réel d'absence prolongée sans dégradation"),
            Palier("7.2", "Choix de trajectoire finale", "Déterminer la forme de l'aboutissement", "Décision documentée (IPO/acquisition/indépendance)"),
        ],
        gate_sortie=Gate(
            id="final",
            must_meet=[
                _c("gouvernance_distribuee", "Gouvernance/opérations ne dépendent plus d'une seule personne"),
                _c("trajectoire_poursuivie", "La trajectoire choisie est activement poursuivie, pas juste envisagée"),
            ],
            should_meet=[
                _c("survit_depart_fondateur", "La boîte peut survivre au départ volontaire du fondateur"),
            ],
            opportunites_pertinentes=["ipo", "acquisition_strategique", "transition_gouvernance"],
        ),
    ),
]


def get_phase(numero: int) -> Phase:
    for p in PHASES:
        if p.numero == numero:
            return p
    raise ValueError(f"Phase {numero} inconnue")


# Cadence attendue (jours entre deux activités) par phase — heuristique v1,
# affinable plus tard par archétype/historique réel de l'utilisateur (cold start, cf. architecture).
CADENCE_ATTENDUE_JOURS = {
    0: 3, 1: 3, 2: 4, 3: 7, 4: 5, 5: 10, 6: 14, 7: 14,
}
