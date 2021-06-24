def sortNums(nums):
    #given that we KNOW the list only contains the 3 digits 1,2,3...

    numOnes = 0
    numTwos = 0
    
    for i in range(0, len(nums)):
        current = nums[i]
        if(current == 1):
            if(i > numOnes):
                #means we need to swap @ numOnes
                temp = nums[numOnes]
                nums[numOnes] = nums[i]
                nums[i] = temp
            numOnes += 1
        if(current == 2):
            if(i > numOnes + numTwos):
                #means we need to swap @ numOnes + numTwos
                temp = nums[numOnes + numTwos]
                nums[numOnes + numTwos] = nums[i]
                nums[i] = temp
            numTwos += 1
    return nums  
print(sortNums([3, 3, 2, 1, 3, 2, 1]))
# [1, 1, 2, 2, 3, 3, 3]
#sort in linear O(n) time - meaning cannot traverse list more than once
