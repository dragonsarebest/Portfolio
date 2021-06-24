class Solution:
    def __init__(self):
        self.buckets = {}

    def lengthOfLongestSubstring(self, s):
        lengths = [0]
        self.buckets = {}
        index = 0

        #uses a dictionary like a set, if you try to add a key that already exists 
        #it stops counting the substring length for that section

        for letter in s:
            if(letter in self.buckets.keys()):
                index += 1
                lengths.append(0)
                self.buckets = {}
            else:
                self.buckets[letter] = None
                lengths[index] += 1
        return max(lengths)
print(Solution().lengthOfLongestSubstring('abrkaabcdefghijjxxx'))
# 10
