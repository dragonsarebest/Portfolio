class Solution:
    def longestPalindrome(self, s):
        # Fill this in.

        foundPalindromes = []
        
        #chose a letter on one end.
        #search for the next instance of that letter starting at other end
        #if no other letter is found cut it off
        #if one is found check if its a palindrome going inward

        for i in range(0, len(s)):
            letterToFind = s[i]
            for j in range(len(s)-1, i-1, -1):
                if(s[j] == s[i]):
                    #we found a matching letter - now check if this is a palindrome
                    if(i == j):
                        sub = s[i]
                    else:
                        sub = s[i:j+1]
                    if(self.checkPalindrome(sub)):
                        foundPalindromes.append(sub)
                        print(sub)

        foundPalindromes = sorted(foundPalindromes, key=lambda x: len(x), reverse = True)
        return foundPalindromes[0]
    
    def checkPalindrome(self, s):
        while(len(s) > 0):
            if(s[0] != s[len(s)-1]):
                return False
            else:
                s = s[1:-1]
        return True
# Test program
s = "tracecars"
print(str(Solution().longestPalindrome(s)))
# racecar

s = "abaaa"
print(str(Solution().longestPalindrome(s)))
