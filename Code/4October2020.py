class Solution:
    def getRange(self, arr, target):
        # Fill this in.
        answer = [-1, -1]
        rangeToSearch = [0, len(arr)]

        oldPivot = None
        while(True):
            pivot = sum(rangeToSearch) - 1

            pivot //= 2

            if(oldPivot == pivot):
                break

            if(target > arr[pivot]):
                rangeToSearch[0] = pivot
            elif(target < arr[pivot]):
                rangeToSearch[1] = pivot
            else:
                #we found a match stop
                break

            oldPivot = pivot

        #we do a form of binary search to cut down the number of look ups
        for i in range(*rangeToSearch):
            if(arr[i] == target):
                answer[0] = i
                break
        #find start of the run og target numbers
        
        if(answer[0] != -1):     
            for i in range(rangeToSearch[1]-1, answer[0], -1):
                if(arr[i] == target):
                    answer[1] = i
                    break
        #finds the end beging at the end of the known area up to the fist number we found
        return answer
# Test program 
arr = [1, 2, 2, 2, 2, 3, 4, 7, 8, 8]
x = 2
print(Solution().getRange(arr, x))
# [1, 4]

arr = [100, 150, 150, 153]
x = 150
print(Solution().getRange(arr, x))
# [1, 2]

arr = [1,3,3,5,7,8,9,9,9,15]
x = 9
print(Solution().getRange(arr, x))
# [6, 8]

arr = [1,2,3,4,5,6,10]
x = 9
print(Solution().getRange(arr, x))
# [-1,-1]
