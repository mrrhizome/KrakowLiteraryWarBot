import csv
import random
import collections

#import database from files

fwriters = open("writers.csv", newline='', encoding='utf8', errors='ignore')
writersData = list(csv.reader(fwriters, delimiter=';'))

fpersona = open("persona.csv", newline='', encoding='utf8', errors='ignore')
personaData = list(csv.reader(fpersona, delimiter=';'))

frulingClass = open("rulingclass.csv", newline='', encoding='utf8', errors='ignore')
rulingData = list(csv.reader(frulingClass, delimiter=';'))

fevents = open("events.csv", newline='', encoding='utf8', errors='ignore')
eventsData = list(csv.reader(fevents, delimiter=';'))

turnWinner = []
books = {}
inflection = {}
links={}

for row in writersData:
    writer = str(row[0])
    book = str(row[1])
    books[writer] = book
    inflection[writer]= str(row[2])
    links[writer] = str(row[3])


#initial count
cnt = collections.Counter()
for row in writersData:
    writer = str(row[0])
    cnt[writer] += 1

turn=1
fight=0
dailyTurnCnt = 1
weekDay = 1
weekCnt = 1

isSpecialWeek = 0

#definitions

def conquer(wonWriter, lostWriter, gameCnt):
    
    #let's build a list for the announcement's sentences
    personaIndex = random.randint(0,len(personaData)-1)
    persona = personaData[personaIndex][0]
        
    verbIndex = random.randint(0,len(personaData)-1)
    verb = personaData[verbIndex][1]
    
    global fight
    
    #woah, multiple wins
    if fight > 3 and wonWriter==turnWinner[fight-1] and wonWriter==turnWinner[fight-2] and wonWriter==turnWinner[fight-3] and wonWriter==turnWinner[fight-4]:
        print(wonWriter, "kontynuuje podboje, dorównując legendarnym wojownikom i wojowniczkom FEJMu.")
    elif fight > 2 and wonWriter==turnWinner[fight-1] and wonWriter==turnWinner[fight-2] and wonWriter==turnWinner[fight-3]:
        print(wonWriter, "jest w bitewnym szale. Lepiej poznaj, kto zacz. ", links[wonWriter])
    elif fight > 1 and wonWriter==turnWinner[fight-1] and wonWriter==turnWinner[fight-2]:
        print("Ło cie pierona, ", wonWriter, "nie zamierza się zatrzymać i zdobywa już trzecie terytorium.")
    elif fight > 0 and wonWriter==turnWinner[fight-1]:
        print(wonWriter, "ponownie zwycięża!")
    

    #praise the winner
    if gameCnt[lostWriter] == 1:
            print('⚔️ {} podbija ławkę {} ⚔️ \n{} {} utwór „{}”.'.format(wonWriter, inflection[lostWriter], persona, verb, books[wonWriter]))
    else:
            print('⚔️ {} podbija ławki {} ⚔️ \n{} {} utwór „{}”.'.format(wonWriter, inflection[lostWriter], persona, verb, books[wonWriter]))

    
    #erase the loser          
    i=0
    for row in writersData:
        if str(writersData[i][0]) == lostWriter:
            row[0]=wonWriter
            row[1]=books[wonWriter]
            row[2]=inflection[wonWriter]
            gameCnt[wonWriter] += 1
            gameCnt[lostWriter] -= 1
        i = i+1
    
    #summary
    rulingIndex = random.randint(0,len(rulingData)-1)
    ruling = rulingData[rulingIndex][0]
    print("{} {} {} ławkami.".format(wonWriter, ruling, gameCnt[wonWriter]))
    
    if len(gameCnt.keys()) > 2:
        print("\nNa placu boju pozostaje", len(cnt.keys())-1, "pisarzy i pisarek.")
    
    fight += 1
    turnWinner.append(wonWriter)

def showStats ():
    
    writersLeft = len(cnt.keys())
    
    if writersLeft > 10:
        print("\n💪 Najwięcej ławek mają teraz:")
        for i in range(0,10):
            if cnt.most_common()[i][1] != 1:
                line = str(i+1) + ". " + cnt.most_common()[i][0] + " – " + str(cnt.most_common()[i][1])
                print(line)
    elif writersLeft > 2:
        print("\n💪 Najwięcej ławek mają teraz:")
        for i in range(0,writersLeft):
            if cnt.most_common()[i][1] != 0:
                line = str(i+1) + ". " + cnt.most_common()[i][0] + " – " + str(cnt.most_common()[i][1])
                print(line)


#main loop

while cnt.most_common()[0][1] < len(writersData):
    
    #count the points
    cnt = collections.Counter()
    for row in writersData:
        writer = str(row[0])
        cnt[writer] += 1
    
    
    #greater chance for the last winner (if true don't randomize the winner)
    strongChance = random.randint(1,10)
    
    #a chance that a person with much less points will conquer a bigger player
    luckyShot = random.randint(1,5)

    #special event?
    isSpecialTurn = 0
    if len(eventsData) != 0:
        isSpecialTurn = random.randint(1,10)
    
    #choose the winner and the loser
    weHaveWinner = False
    while not weHaveWinner:
        if  turn == 1 or strongChance >= 3:
            won = random.choice(list(cnt.keys()))
        
        lost = random.choice(list(cnt.keys()))
        
        #winner/loser ratio
        fairRatio = False
        difference = float(cnt[won])/float(cnt[lost])
        if difference > 0.2:
            fairRatio = True

        if won != lost and (fairRatio or luckyShot == 1):
            weHaveWinner = True
    
    
    #print("\nTura {}, runda {}, dzień {}, tydzień {}".format(turn, dailyTurnCnt, weekDay, weekCnt))
        
    
    # first turn - always a fight
    if turn == 1:
        conquer(won, lost, cnt) 
    
    # special event?
    elif isSpecialTurn == 1:
        eventIndex = random.randint(0,len(eventsData)-1)
        event = eventsData[eventIndex][0]
        print("✨ Wydarzenie specjalne ✨")
        print(event)
        del eventsData[eventIndex]

    # if no special event - a fight
    else:
        conquer(won, lost, cnt)

    #show statistics (once a day)
    if dailyTurnCnt == 7 or len(cnt.keys()) < 11:
        showStats()
 
    #time counter
    turn +=1
    dailyTurnCnt+=1
    if dailyTurnCnt == 8: 
        dailyTurnCnt = 1
                        
        weekDay +=1
        if weekDay == 8:
            weekDay = 1
            weekCnt += 1
        
    print("\n")
        

fwriters.close()
fpersona.close()
frulingClass.close()

print("👑💎🏆 ", won, "zagarnia wszystkie ławki i wygrywa wojnę o FEJM! 👑💎🏆 ")

#print the results to the file
#with open("writers2.csv", "w", newline="", encoding="utf-8") as fwriters:
#   writer = csv.writer(fwriters, delimiter = ";")
#   writer.writerows(writersData)
#fwriters.close()