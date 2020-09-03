from random import *

from tkinter import *
from tkinter import filedialog

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

# GUI erstellen

def updateStrength():
    selected = choiceStrength.get()
    if selected == 1:
        selectFileButton.config(state = 'disabled')
        playerCountEntry.config(state = 'normal')
    elif selected == 2:
        selectFileButton.config(state = 'normal')
        playerCountEntry.config(state = 'disabled')

def fileButtonAction():
    fileName = filedialog.askopenfilename(initialdir ='C:', title='Datei öffnen', filetypes=(('Text Dateien', '.txt'),('Alle Dateien','*.*')))
    print(fileName)

root = Tk()

root.title('Tunier Simulator (Aufgabe 3)')

rootFrame = Frame(root)
rootFrame.pack(pady = 5)

chkTypeColor = '#66e8ff'
chkTypeFrame = LabelFrame(rootFrame, bg = chkTypeColor, text = 'Turnierform wählen')
chkTypeFrame.pack(fill = BOTH, padx = 10, pady = 10)

choiceType = IntVar()
chkTypeLeague = Radiobutton(chkTypeFrame, text = 'Liga', variable = choiceType, value = 1, bg = chkTypeColor, activebackground = chkTypeColor)
chkTypeLeague.grid(row = 0, sticky = W, pady = 5)

chkTypeKO = Radiobutton(chkTypeFrame, text = 'K.O. Tunier', variable = choiceType, value = 2, bg = chkTypeColor, activebackground = chkTypeColor)
chkTypeKO.grid(row = 1, sticky = W, pady = 5)

chkStrengthColor = '#ffff80'
chkStrengthFrame = LabelFrame(rootFrame, bg = chkStrengthColor, text = 'Spielerstärken')
chkStrengthFrame.pack(fill = BOTH, padx = 10, pady = 10)

choiceStrength = IntVar()
chkStrengthRandom = Radiobutton(chkStrengthFrame, text = 'zufällig', variable = choiceStrength, value = 1, bg = chkStrengthColor, activebackground = chkStrengthColor, command = updateStrength)
chkStrengthRandom.grid(row = 0, sticky = W, pady = 5)

playerCountFrame = Frame(chkStrengthFrame, bg = chkStrengthColor)
playerCountFrame.grid(row = 0, column = 1, sticky = W, pady = 5, padx = 5)

playerCountLabel = Label(playerCountFrame, text = 'Spieler 2^', bg = chkStrengthColor)
playerCountLabel.pack(side = LEFT)

playerCountEntry = Entry(playerCountFrame, width = 10, state = 'disabled')
playerCountEntry.pack(side = LEFT)

chkStrengthFile = Radiobutton(chkStrengthFrame, text = 'aus Datei', variable = choiceStrength, value = 2, bg = chkStrengthColor, activebackground = chkStrengthColor, command = updateStrength)
chkStrengthFile.grid(row = 1, sticky = W, pady = 5)

selectFileButton = Button(chkStrengthFrame, text = 'Datei auswählen', state = 'disabled', command = fileButtonAction)
selectFileButton.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

startSimButton = Button(rootFrame, text = 'Simulieren')
startSimButton.pack()

resultColor = '#77ff33'
resultFrame = LabelFrame(rootFrame, text = 'Ergebnisse des Tuniers', bg = resultColor)
resultFrame.pack(fill = BOTH, pady = 10, padx = 10)

resultIndexTxtLabel = Label(resultFrame, text = 'Gewinnerindex:', bg = resultColor)
resultIndexTxtLabel.grid(row = 0, sticky = W)

resultIndexValLabel = Label(resultFrame, text = '7', bg = '#cccccc')
resultIndexValLabel.grid(row = 0, column = 1, sticky = W)

resultStrengthTxtLabel = Label(resultFrame, text = 'Gewinnerstärke:', bg = resultColor)
resultStrengthTxtLabel.grid(row = 1, sticky = W)

resultStrengthValLabel = Label(resultFrame, text = '7', bg = '#cccccc')
resultStrengthValLabel.grid(row = 1, column = 1, sticky = W)

root.mainloop()