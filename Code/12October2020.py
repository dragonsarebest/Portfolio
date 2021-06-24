class MaxStack:
    def __init__(self):
        # Fill this in.
        self.array = []

    def push(self, val):
        self.array.append(val)

    def pop(self):
        return self.array.pop()

    def max(self):
        return max(self.array)

s = MaxStack()
s.push(1)
s.push(2)
s.push(3)
s.push(2)
print(s.max())
# 3
s.pop()
s.pop()
print(s.max())
# 2
