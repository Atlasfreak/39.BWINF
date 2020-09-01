from random import *

def fight(strengthP1, strengthP2):
    # strengthP1 = int
    # strengthP2 = int
    #
    # Simuliere einen Kampf zwischen 2 Spielern.

    rand = randint(1, strengthP1 + strengthP2)
    if rand <= strengthP2:
        #print("Spieler 2 hat gewonnen!")
        return True
    elif rand - strengthP2 <= strengthP1:
        #print("Spieler 1 hat gewonnen!")
        return False

def simulateFights(strengthP1, strengthP2, times):
    # strengthP1 = int
    # strengthP2 = int
    # times = int
    # 
    # Simuliere times Kämpfe zwischen 2 Spielern.


    winsP1 = 0
    winsP2 = 0
    for i in range(times):
        if fight(strengthP1, strengthP2):
            winsP2 += 1
        else:
            winsP1 += 1
    return (winsP1/winsP2, winsP1, winsP2)