#You are given an array of integers in an arbitrary order.
#Return whether or not it is possible to make the array
#non-decreasing by modifying at most 1 element to any value.
def check(lst):
    # Fill this in.
    numErrors = 0

    for i in range(0, len(lst)-1):
        if(lst[i+1] < lst[i]):
            numErrors += 1
        if(numErrors > 1):
            return False
    return True

print(check([13, 4, 7]))
# True
print(check([5,1,3,2,5]))
# False
