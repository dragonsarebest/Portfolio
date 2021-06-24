#Given a list of numbers, where every number shows up twice except for
#one number, find that one number.
def singleNumber(nums):
    for i in range(0, len(nums)):
        findAgain = nums.pop(i)
        if(findAgain in nums):
            continue
        else:
            return findAgain

print(singleNumber([4, 3, 2, 4, 1, 3, 2]))
# 1
