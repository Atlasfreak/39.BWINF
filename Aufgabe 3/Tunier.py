from random import *

def fight(strengthP1, strengthP2):
    '''  
    strengthP1 = int
    strengthP2 = int
    
    True wenn Spieler 2 gewinnt
    False wenn Spieler 1 gewinnt
    '''

    rand = randint(1, strengthP1 + strengthP2)
    if rand <= strengthP2:
        # Spieler 2
        return True
    elif rand - strengthP2 <= strengthP1:
        # Spieler 1
        return False

def simulateFights(strengthP1, strengthP2, times):
    '''
    strengthP1 = int
    strengthP2 = int
    times = int
    
    Simuliere times Kämpfe zwischen 2 Spielern.
    '''

    winsP1 = 0
    winsP2 = 0
    for i in range(times):
        if fight(strengthP1, strengthP2):
            winsP2 += 1
        else:
            winsP1 += 1
    return (winsP1/winsP2, winsP1, winsP2)

def league(playerStrengthList):
    '''
    playerStrengthList = list

    Simuliert ein Liga in der jeder Spieler gegen jeden anderen Spieler antritt.
    Gibt den Gewinner der Liga zurück.
    '''
    wins = [0] * len(playerStrengthList)
    
    for p1 in range(len(playerStrengthList)-1):
        for p2 in range(p1+1, len(playerStrengthList)):

            print(playerStrengthList[p1], playerStrengthList[p2])
            if fight(playerStrengthList[p1], playerStrengthList[p2]):
                wins[p2] += 1
            else:
                wins[p1] += 1
    winner = wins.index(max(wins))
    return winner

def createPlayerStrength2DList(playerStrengthList):
    '''
    playerStrengthList = list

    Erstellt eine 2D Liste nach dem Schema [[indexUrpsrung1, WertUrsprung1], [indexUrpsrung2, WertUrsprung2], ...]

    Dies wird benötigt um am Ende eines Tuniers zu ermitteln welcher Spieler gewonnen hat und
    nicht nur die Kampfstärke zu erhalten.
    '''
    playerStrength2DList = []
    for i in range(len(playerStrengthList)):
        playerStrength2DList.append([i, playerStrengthList[i]])
    return playerStrength2DList

def k_o_round(playerStrength2DList, count):
    '''
    playerStrength2DList = list # Schema [[indexUrpsrung1, WertUrsprung1], [indexUrpsrung2, WertUrsprung2], ...]
    count = int                 # muss ungerade sein

    Simuliert eine K.O. Runde mit beliebiger Anzahl an Kämpfen
    und gibt eine 2D Liste mit allen verbleibenden Spielern zurück.
    '''
    remainingPlayerStrength2DList = []
    for p in range(0,len(playerStrength2DList),2):
        p1 = playerStrength2DList[p]
        winsP1 = 0
        p2 = playerStrength2DList[p+1]
        winsP2 = 0
        counter = count
        while counter > 0:
            if fight(p1[1], p2[1]):
                winsP2 += 1
            else:
                winsP1 += 1
            counter -= 1
            print(winsP1, winsP2)
        if winsP1 > winsP2:
            remainingPlayerStrength2DList.append(p1)
        elif winsP2 > winsP1:
            remainingPlayerStrength2DList.append(p2)
        print(remainingPlayerStrength2DList)

    return remainingPlayerStrength2DList

def k_o_tournament(playerStrengthList, fightCount):
    '''
    playerStrengthList = list
    fightCount = int            # muss ungerade sein

    Simuliert ein K.O. Tunier.
    Gibt die ID des Gewinners aus.
    '''
    playerStrength2DList = createPlayerStrength2DList(playerStrengthList)
    while len(playerStrength2DList) > 1:
        playerStrength2DList = k_o_round(playerStrength2DList, fightCount)
    print(playerStrength2DList)
    winner = playerStrength2DList[0][0]
    return winner