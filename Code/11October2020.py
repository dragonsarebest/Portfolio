#invert binary tree. left->right. right->left
class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
    def preorder(self):
        print(self.value)
        if(self.left):
            self.left.preorder()
        if(self.right):
            self.right.preorder()

def invert(node):
    # Fill this in.

    temp = node.right
    node.right = node.left
    node.left = temp

    if(node.right):
        invert(node.right)
    if(node.left):
        invert(node.left)

root = Node('a') 
root.left = Node('b') 
root.right = Node('c') 
root.left.left = Node('d') 
root.left.right = Node('e') 
root.right.left = Node('f') 

root.preorder()
# a b d e c f 
print("\n")
invert(root)
root.preorder()
# a c f b e d
