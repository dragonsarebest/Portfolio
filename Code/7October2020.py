# You are given a list of numbers, and a target number k.
#Return whether or not there are two numbers in the list that add up to k.

def two_sum(theList, k):
    # do this in constant time....
    possibleAnswers = {}
    for i in range(0, len(theList)):
        if((k - theList[i]) in possibleAnswers):
            return True
        possibleAnswers[theList[i]] = 0
        #add it to a dic which is a hash table w/ constant lookup time
        #add each necessary compliment to the hashmap

print(two_sum([4,7,1,-3,2], 5))
# True
