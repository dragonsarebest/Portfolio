class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

def findCeilingFloor(root_node, k, floor=None, ceil=None):
    current_node = root_node

    if((ceil == None or current_node.value < ceil )and current_node.value >= k):
        ceil = current_node.value
    if(( floor == None or current_node.value > floor) and current_node.value <= k):
        floor = current_node.value

    if(current_node.left):
        floor, ceil = findCeilingFloor(current_node.left, k, floor, ceil)
    if(current_node.right):
        floor, ceil = findCeilingFloor(current_node.right, k, floor, ceil)
      
    return (floor, ceil)

root = Node(8) 
root.left = Node(4) 
root.right = Node(12) 
  
root.left.left = Node(2) 
root.left.right = Node(6) 
  
root.right.left = Node(10) 
root.right.right = Node(14)  

print(findCeilingFloor(root, 5))
# (4, 6)
