"""
Calcul du thème natal sidéral — Swiss Ephemeris, ayanamsa Lahiri par défaut.
Source de la décision : fhq-architecture-v1.md, section 7.
Usage optionnel — jamais dans les critères de gate, seulement onboarding + calendrier.
"""

import swisseph as swe

PLANETES = {
    "Soleil": swe.SUN, "Lune": swe.MOON, "Mercure": swe.MERCURY,
    "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
    "Saturne": swe.SATURN, "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE,
    "Pluton": swe.PLUTO,
}

AYANAMSAS = {
    "lahiri": swe.SIDM_LAHIRI,
    "fagan_bradley": swe.SIDM_FAGAN_BRADLEY,
    "krishnamurti": swe.SIDM_KRISHNAMURTI,
    "raman": swe.SIDM_RAMAN,
}


def calculer_theme_natal(annee: int, mois: int, jour: int, heure: float,
                          latitude: float, longitude: float, ayanamsa: str = "lahiri") -> dict:
    """
    heure : décimale UTC (ex: 14.5 pour 14h30)
    Retourne les positions sidérales (longitude écliptique en degrés) de chaque planète.
    """
    if ayanamsa not in AYANAMSAS:
        raise ValueError(f"Ayanamsa inconnu : {ayanamsa}. Options : {list(AYANAMSAS.keys())}")

    swe.set_sid_mode(AYANAMSAS[ayanamsa])
    jd = swe.julday(annee, mois, jour, heure)

    positions = {}
    for nom, code in PLANETES.items():
        resultat = swe.calc_ut(jd, code, swe.FLG_SIDEREAL)[0]
        lon_sid = resultat[0]
        positions[nom] = round(lon_sid, 4)

    ascendant_data = swe.houses_ex(jd, latitude, longitude, b'P', flags=swe.FLG_SIDEREAL)
    ascendant = round(ascendant_data[0][0], 4)

    return {
        "date_utc": f"{annee}-{mois:02d}-{jour:02d}",
        "heure_utc": heure,
        "latitude": latitude,
        "longitude": longitude,
        "ayanamsa": ayanamsa,
        "positions_planetes": positions,
        "ascendant": ascendant,
    }


def signe_depuis_longitude(longitude_deg: float) -> str:
    signes = ["Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
              "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"]
    index = int(longitude_deg // 30) % 12
    return signes[index]
