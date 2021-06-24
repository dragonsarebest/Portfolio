class ListNode(object):

    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:

    def __init__(self):
        self.answer = None
        self.start = None
    
    def addTwoNumbers(self, l1, l2, c = 0):
        while(True):
            if(c == 0):
                self.answer = ListNode(0)
                self.start = self.answer
                #intialize to 0

            if(not l1  and not l2):
                #we are done here, return value
                if(self.answer.val == 0):
                    #remove leading 0 as it is not part of the answer
                    self.answer = self.start
                    for i in range(0, c-1):
                        self.answer = self.answer.next
                    self.answer.next = None
                return self.start 

            if(not l1):
                summation = 0
            else:
                summation = l1.val

            if(l2):
                summation += l2.val

            #since we dont assume both lists are equal size, if one runs out treat it as a 0

            self.answer.val += summation
            #add current sum up
            
            summation = self.answer.val - self.answer.val % 10
            self.answer.val %= 10
            #we only want the one's place (any more than 1 digit becomes a caryover)

            summation //= 10
            #divide cary over by 10 to get the caryover amount
            self.answer.next = ListNode(summation)
            self.answer = self.answer.next
            c += 1

            if(l1):
                l1 = l1.next
            if(l2):
                l2 = l2.next
            #if not none, increment linked lists
    
l1 = ListNode(2)
l1.next = ListNode(4)
l1.next.next = ListNode(3)

l2 = ListNode(5)
l2.next = ListNode(6)
l2.next.next = ListNode(4)

result = Solution().addTwoNumbers(l1, l2)

while result:
    print (result.val)
    result = result.next
