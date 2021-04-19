"""

Seven envelopes are placed randomly at each seat position of a round table that can be easily rotated. Each envelope contains the name of one of seven people. Each envelope contains exactly one name and each person's name is in one of the envelopes.

The seven people each take a seat at the table in front of one of the envelopes. If at least two people are seated in front of the envelope containing their name, all seven people win The Prize. If not, they are permitted to rotate the table as much as they like, so long as they not change the relative order of the envelopes on the table. If they are successful in matching two of the people and their envelopes, then the group still wins.

Suppose at the start that none of the seven people are seated in front of the correct envelope. What is the probability that the group can win The Prize?

"""
noMatchAtStart = []

possibleSeating = []
#7! * 7! number of combinations b/w seating & envelops

sevenFactorial = 7*6*5*4*3*2*1*1


def checkWinnable(answer, seating):
    for i in range(0, len(seating)):
        tempSeating = seating[i:len(seating)]
        tempSeating.extend(seating[0:i])
        #print(tempSeating)
        numRight = 0
        #print(tempSeating, answer, end = ":")
        for j in range(0, len(answer)):
            #print(answer[j])
            #print(seating[j])
            if(answer[j] == seating[j]):
                numRight += 1
            if(numRight >= 2):
                return True
        #print(numRight)
    return False


inProgress = []
done = []
numInitZero = []

current = [0,0,0,0,0,0,0]
inProgress.append(current)

while(True):
    current = inProgress.pop()
    numEmpty = current.count(0)
    if(numEmpty == 0):
        done.append(current)
    else:
        num = max(current)+1
        for i in range(0, len(current)):
            temp = []
            temp.extend(current)
            if(temp[i] != 0):
                continue
            temp[i] = num
            inProgress.append(temp)
    if(len(inProgress) == 0):
        break

for j in range (0, len(done)):
    seating = done[j]
    for k in range (0, len(done)):
        answer = done[k]
        foundOne = False
        for i in range(0, len(seating)):
            if(seating[i] == answer[i]):
                foundOne = True
                break
        if(foundOne == False):
            numInitZero.append([j, k])

#probabilityOfStartingWithZero = len(numInitZero) / (sevenFactorial*sevenFactorial)
numWinnable = 0
#done.sort()
#print(done)
numNotWinnable = 0
for poss in numInitZero:
    if(checkWinnable(done[1], done[0])):
        numWinnable += 1
    else:
        numNotWinnable += 1
print(numNotWinnable)
print(numWinnable)
probabilityOfWinningWithZero = numWinnable/len(numInitZero)
print(probabilityOfWinningWithZero)

