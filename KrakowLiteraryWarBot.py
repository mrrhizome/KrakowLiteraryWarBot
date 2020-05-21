import csv
import random
import collections

fwriters = open("writers.csv", newline='', encoding='utf8', errors='ignore')
writersdata = list(csv.reader(fwriters, delimiter=';'))

fpersona = open("persona.csv", newline='', encoding='utf8', errors='ignore')
personaData = list(csv.reader(fpersona, delimiter=';'))

books = {}
for row in writersdata:
    book = str(row[1])
    writer = str(row[0])
    books[writer] = book

bestwritercount = 1

while bestwritercount < len(writersdata):
    
    cnt = collections.Counter()
    for row in writersdata:
        writer = str(row[0])
        cnt[writer] += 1
        

    #greater chance for the biggest owner
    strongchance = random.randint(1,10)    
    
    if  strongchance >= 3 or bestwritercount == 1:
        won = random.choice(list(cnt.keys()))
         
    lost = random.choice(list(cnt.keys()))
    
    
    if won != lost:
 
        personaIndex = random.randint(1,len(personaData)-1)
        persona = personaData[personaIndex][0]    

        #summaries
        
        print('{} podbija ławki {}. {} czytają do upadłego utwór „{}”.'.format(won, lost, persona, books[won]))

        i=0
        for row in writersdata:
            if str(writersdata[i][0]) == lost:
                row[0]=won
                row[1]=books[won]
            i = i+1
        
        cnt = collections.Counter()
        for row in writersdata:
            writer = str(row[0])
            cnt[writer] += 1

        print("\n{} dzierży teraz władzę nad {} ławkami".format(won, cnt[won]))

        bestwritercount = int(cnt.most_common()[0][1])
        bestwriter = str(cnt.most_common()[0][0])

        print("Na placu boju pozostało {} pisarzy i pisarek".format(len(cnt.keys())))
        #print("\nNajwięcej ławek ma teraz {} ({}).".format(cnt.most_common()[0][0], bestwritercount))
        
    
fwriters.close()
fpersona.close()

print(won, "wygrywa!")
#now the winning writer has to take the loser's place in the file

with open("writers2.csv", "w", newline="", errors='ignore') as fwriters:
   writer = csv.writer(fwriters, delimiter = ";")
   writer.writerows(writersdata)

fwriters.close()