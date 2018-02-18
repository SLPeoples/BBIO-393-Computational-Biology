
"""
Write a new class that represents the nodes
in a phylogenetic tree

Each node should know:

"""

class TreeNode(object):
    """A node in a phylogenetic tree
    
    Each node will have a name, traits
    children, and parent
    """
    
    def __init__(self,name,traits=None,children=None,parent=None):
        print("I am a TreeNode!")
        self.Name = name
        print("My name is:",self.Name)
        self.Children = children
        print("My children are:",str(self.Children))


A = TreeNode("A")
B = TreeNode("B")
AB = TreeNode("AB", children = [A,B])

print("Now list all of ABs children")
for node in AB.Children:
    print(node.Name)

  
