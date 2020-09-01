from random import *

def createUrn(strengthP1, strengthP2):
    # Urne mit Kugeln basierend auf Spieler Stärke generieren
    urn = []
    while (strengthP1 + strengthP2) > 0:
        if randint(0,2) and strengthP1 > 0:
            # Kugel für Spieler 1 hinzufügen
            urn.append(0)
            strengthP1 -= 1
        elif strengthP2 > 0:
            # Kugel für Spieler 2 hinzufügen
            urn.append(1)
            strengthP2 -= 1

    return urn

