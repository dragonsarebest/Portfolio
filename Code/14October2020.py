#do 3 numbers exist in this list (a,b,c...) such that a^2 + b^2 = c^2
def findPythagoreanTriplets(nums):
    answers = {}
    for i in range(0, len(nums)):
        for j in range(i+1, len(nums)):
            if((nums[i]**2 + nums[j]**2)**0.5 in nums):
                return True
    return False
print(findPythagoreanTriplets([3, 12, 5, 13]))
# True
