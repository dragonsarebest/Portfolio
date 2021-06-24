#Given two strings, determine the edit distance between them.
#The edit distance is defined as the minimum number of edits
#(insertion, deletion, or substitution)
#needed to change one string to the other.

#For example, "biting" and "sitting" have an edit distance of 2
#(substitute b for s, and insert a t).

def distance(s1, s2):
    #if they are the same length, the distance = num diff characters
    num = 0

    if(len(s2) > len(s1)):
        temp = s1
        s1 = s2
        s2 = temp
    
    while(s1 != s2):
        #insertion & deletion are the "same"
        if(len(s1) > len(s2)):
            #then we need to remove a character from s1
            bestOption = None
            bestDist = None
            for i in range(0, len(s1)):
                current = s1

                #if we only try deleting incorrect characters then we may be too greedy and make it take more changes than needed
                
                #try every option - delete one character to see if it improves
                current = current[:i] + current[i+1:]
                
                option = distance(current, s2)
                
                if(bestDist == None or option < bestDist):
                    bestDist = option
                    bestOption = current
            s1 = bestOption
            num += 1

        else:
            #means same length - now we try swapping...
            for i in range(0, len(s1)):
                if(s1[i] != s2[i]):
                    #s1[i] = s2[i]
                    s1 = s1[:i] + s2[i] + s1[i+1:]
                    num += 1
    return num

print(distance('biting', 'sitting'))
# 2
