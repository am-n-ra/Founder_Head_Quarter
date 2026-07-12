"""
Bibliothèque d'archétypes — couche variable du modèle à deux couches.
Le squelette (schema.py) est fixe. Ici : ce qui varie par type de venture.
Source : section "BIBLIOTHÈQUE D'ARCHÉTYPES" de fhq-formule-phases-v1.md
"""

from dataclasses import dataclass


@dataclass
class Archetype:
    cle: str
    nom: str
    preuve_pmf_dominante: str
    vecteur_distribution_typique: str
    piege_phase5: str


ARCHETYPES = {
    "saas": Archetype(
        cle="saas", nom="SaaS (logiciel en abonnement)",
        preuve_pmf_dominante="Rétention nette (NRR), fréquence d'usage, expansion de compte",
        vecteur_distribution_typique="Niche → Open, product-led growth ou sales-led selon ticket",
        piege_phase5="Scaler l'acquisition avant que le churn soit compris",
    ),
    "marketplace": Archetype(
        cle="marketplace", nom="Marketplace / Index (deux faces ou plus)",
        preuve_pmf_dominante="Liquidité des deux côtés (offre ET demande actives simultanément)",
        vecteur_distribution_typique="Niche géographique/verticale d'abord, Big Fish si un acteur peut amorcer l'offre",
        piege_phase5="Scaler la demande sans avoir résolu la liquidité de l'offre (ou l'inverse)",
    ),
    "infra_deeptech": Archetype(
        cle="infra_deeptech", nom="Infra / Deep-tech (modèles propriétaires, R&D lourde)",
        preuve_pmf_dominante="Adoption par intégrateurs/partenaires techniques ; qualité mesurable vs alternatives",
        vecteur_distribution_typique="Big Fish quasi-systématique ; financement recherche = distribution-investisseurs",
        piege_phase5="Confondre excellence technique et adoption réelle",
    ),
    "fintech_reglemente": Archetype(
        cle="fintech_reglemente", nom="Fintech réglementé",
        preuve_pmf_dominante="Conformité réglementaire comme prérequis avant même la rétention ; confiance perçue",
        vecteur_distribution_typique="Partenariats institutionnels quasi-obligatoires ; Incorporation souvent Day One/Trigger précoce",
        piege_phase5="Scaler avant d'avoir sécurisé les partenariats réglementaires nécessaires au volume",
    ),
    "commerce_physique": Archetype(
        cle="commerce_physique", nom="Commerce physique / Retail",
        preuve_pmf_dominante="Rotation des stocks, panier moyen, taux de retour client physique",
        vecteur_distribution_typique="Niche géographique par nature, expansion par réplication de l'emplacement gagnant",
        piege_phase5="Répliquer un emplacement/concept avant d'avoir isolé ce qui faisait marcher le premier",
    ),
    "service_agence": Archetype(
        cle="service_agence", nom="Service / Agence",
        preuve_pmf_dominante="Taux de renouvellement de contrat, référencement spontané par clients existants",
        vecteur_distribution_typique="Notoriété du fondateur dominante au départ, transition nécessaire vers canal indépendant",
        piege_phase5="Rester dépendant du réseau personnel du fondateur bien après Phase 4",
    ),
}


def get_archetype(cle: str) -> Archetype | None:
    return ARCHETYPES.get(cle)


def list_archetypes() -> list[str]:
    return list(ARCHETYPES.keys())
