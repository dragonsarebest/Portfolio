def waterlog(listOfValues):
    """takes a list of values representing a histogram and outputs the ammount of water it could hold"""
    i = 0
    #current index
    v = listOfValues[0]
    #current value
    i2 = 0
    #temp index
    v2 = 0
    #temp value
    end = len(listOfValues)
    #we shall go till we reach this index
    small = 0
    #ammount of obstacles we need to detract from water
    total = 0
    #total water volume

    for i2 in range(1, end+1):
        #going left
        v2 = listOfValues[i2-1]
        if(v2 >= v and not v2 == 0):
            total += (i2 - i - 1)*v - small
            small = 0
            i = i2
            v = v2
        else:
            small += v2
    if(v > v2):
        #if we've reached the end and we couldnt add any water from this tower, need to go right
        small = 0
        end = i
        i = len(listOfValues)-1
        v = listOfValues[i]
        
        for i2 in range(len(listOfValues), end-1, -1):
            #going right
            v2 = listOfValues[i2-1]
            if(v2 >= v and not v2 == 0):
                total += (i - i2 - 1)*v - small
                small = 0
                i = i2
                v = v2
            else:
                small += v2
    return total

#should be: [0,0,4,0,0,6,0,0,3,0,8,0,2,0,5,2,0,3,0,0] -> 46
print(waterlog([0,0,4,0,0,6,0,0,3,0,8,0,2,0,5,2,0,3,0,0]))
