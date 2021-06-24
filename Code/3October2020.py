class Solution:
    def isValid(self, s):
        openBraces = {'(' : 0, '[' : 0, '{' : 0}
        closedBraces = {')' : 0, ']' : 0, '}' : 0}

        stack = []
    
        for i in range(0, len(s)):
            brace = s[i]
            if(brace in openBraces.keys()):
                openBraces[brace] += 1
                stack.append(brace)
                
            if(brace in closedBraces.keys()):
                closedBraces[brace] += 1

                lastOpen = stack.pop()                
                #if the last open bracket isnt the same type - return false
                if((lastOpen == '[' and brace != ']' or lastOpen == '(' and brace != ')' or lastOpen == '{' and brace != '}')):
                    return False
                    
            #if the number of open & closed brackets dont match
            #then its invalid.

        if(len(stack) != 0):
            return False
        
        return True

# Test Program
s = "()(){(())" 
# should return False
print(Solution().isValid(s))

s = ""
# should return True
print(Solution().isValid(s))

s = "([{}])()"
# should return True
print(Solution().isValid(s))
